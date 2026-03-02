from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import html
import urllib.parse
from typing import Set, List

import requests


YANDEX_API = "https://cloud-api.yandex.net/v1/disk"
DISK_FOLDER = "disk:/Backup"   # папка на Яндекс.Диске
LOCAL_FOLDER = "pdfs"          # локальная папка рядом с server.py
PAGE_LIMIT = 100              # для пагинации списка файлов на Диске

TOKEN = input("Введите OAuth-токен Яндекс.Диска (из полигона): ").strip()


def get_token() -> str:
    if not TOKEN:
        raise RuntimeError("Токен не введён.")
    return TOKEN


def yandex_headers() -> dict:
    return {"Authorization": f"OAuth {get_token()}"}


def ensure_disk_folder_exists() -> None:
    r = requests.put(
        f"{YANDEX_API}/resources",
        headers=yandex_headers(),
        params={"path": DISK_FOLDER},
        timeout=10,
    )
    if r.status_code not in (201, 409):
        r.raise_for_status()


def get_uploaded_names_from_disk() -> Set[str]:
    """Имена объектов внутри DISK_FOLDER на Яндекс.Диске. С пагинацией."""
    uploaded: Set[str] = set()
    offset = 0

    while True:
        params = {
            "path": DISK_FOLDER,
            "limit": PAGE_LIMIT,
            "offset": offset,
            "fields": "_embedded.items.name,_embedded.total",
        }

        r = requests.get(
            f"{YANDEX_API}/resources",
            headers=yandex_headers(),
            params=params,
            timeout=10,
        )

        if r.status_code == 404:
            return set()

        r.raise_for_status()
        data = r.json()

        embedded = data.get("_embedded") or {}
        items = embedded.get("items") or []
        total = embedded.get("total", 0)

        for item in items:
            name = item.get("name")
            if name:
                uploaded.add(name)

        offset += len(items)
        if offset >= total or not items:
            break

    return uploaded


def get_local_files() -> List[str]:
    """Файлы из локальной папки LOCAL_FOLDER."""
    try:
        names = sorted(os.listdir(LOCAL_FOLDER))
    except FileNotFoundError:
        return []

    result = []
    for n in names:
        if os.path.isfile(os.path.join(LOCAL_FOLDER, n)):
            result.append(n)
    return result


def get_upload_href(ya_path: str) -> str:
    """Получаем ссылку (href) для загрузки файла на Яндекс.Диск."""
    r = requests.get(
        f"{YANDEX_API}/resources/upload",
        headers=yandex_headers(),
        params={"path": ya_path, "overwrite": "true"},
        timeout=15,
    )
    r.raise_for_status()
    return r.json()["href"]


def upload_local_file_to_disk(fname: str) -> None:
    """Загружает LOCAL_FOLDER/fname в DISK_FOLDER/fname на Яндекс.Диск."""
    local_path = os.path.join(LOCAL_FOLDER, fname)
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Локальный файл не найден: {local_path}")

    ensure_disk_folder_exists()

    ya_path = f"{DISK_FOLDER}/{fname}"
    href = get_upload_href(ya_path)

    with open(local_path, "rb") as f:
        put_r = requests.put(href, data=f, timeout=120)
    put_r.raise_for_status()


class HttpGetHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        local_files = get_local_files()

        try:
            ensure_disk_folder_exists()
            uploaded = get_uploaded_names_from_disk()
        except Exception as e:
            uploaded = set()
            print("Ошибка при запросе списка файлов с Яндекс.Диска:", e)

        def li_for(fname: str) -> str:
            display = html.escape(fname)
            value = html.escape(fname, quote=True)
            cls = "uploaded" if fname in uploaded else ""
            class_attr = f' class="{cls}"' if cls else ""

            return f"""
              <li{class_attr}>
                <form action="/upload" method="POST" accept-charset="utf-8" style="margin:0;">
                  <input type="hidden" name="fname" value="{value}">
                  <button type="submit" style="all:unset; cursor:pointer; display:block; width:100%; padding:8px 12px;">
                    {display}
                  </button>
                </form>
              </li>
            """

        items_html = "\n".join(li_for(f) for f in local_files)

        page = f"""
        <html>
          <head>
            <meta charset="utf-8">
            <title>Yandex Disk Uploader</title>
            <style>
              .uploaded {{
                background-color: rgba(0, 200, 0, 0.25);
              }}
              li {{
                margin: 8px 0;
                border-radius: 10px;
                list-style: none;
              }}
              ul {{
                padding: 0;
              }}
            </style>
          </head>
          <body>
            <h1>Файлы</h1>
            <p>Зелёным отмечены файлы, которые уже загружены на Яндекс.Диск.</p>
            <ul>
              {items_html if items_html else "<li>В папке pdfs нет файлов</li>"}
            </ul>
          </body>
        </html>
        """

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def do_POST(self):
        if self.path != "/upload":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return

        try:
            content_len = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(content_len).decode("utf-8", errors="replace")

            params = urllib.parse.parse_qs(body)
            fname = params.get("fname", [""])[0].strip()

            if not fname:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"empty filename")
                return

            upload_local_file_to_disk(fname)
            print("Uploaded:", fname)

            self.send_response(303)
            self.send_header("Location", "/")
            self.end_headers()

        except Exception as e:
            print("UPLOAD ERROR:", e)
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"upload error")


def run():
    server = HTTPServer(("", 8000), HttpGetHandler)
    print("Server started: http://127.0.0.1:8000")
    server.serve_forever()


if __name__ == "__main__":
    run()