documents = [
    {'type': 'passport', 'number': '2207 876234', 'name': 'Василий Гупкин'},
    {'type': 'invoice', 'number': '11-2', 'name': 'Геннадий Покемонов'},
    {'type': 'insurance', 'number': '10006', 'name': 'Аристарх Павлов'}
]

directories = {
    '1': ['2207 876234', '11-2'],
    '2': ['10006'],
    '3': []
}

def get_shelf_by_number(number: str) -> str:
    """Возвращает номер полки, на которой лежит документ."""
    for shelf, docs in directories.items():
        if number in docs:
            return shelf
    return None

def get_owner_by_number(number: str) -> str:
    """Возвращает имя владельца по номеру документа."""
    for doc in documents:
        if doc['number'] == number:
            return doc['name']
    return None

def main():
    """Главный цикл обработки команд."""
    print("Программа секретаря. Команды:")
    print("p – узнать владельца по номеру документа")
    print("s – узнать полку хранения по номеру документа")
    print("q – выйти из программы")

    while True:
        command = input("\nВведите команду: ").strip().lower()

        if command == 'p':
            number = input("Введите номер документа: ").strip()
            owner = get_owner_by_number(number)
            if owner:
                print(f"Владелец документа: {owner}")
            else:
                print("Документ не найден.")

        elif command == 's':
            number = input("Введите номер документа: ").strip()
            shelf = get_shelf_by_number(number)
            if shelf:
                print(f"Документ хранится на полке: {shelf}")
            else:
                print("Документ не найден на полках.")

        elif command == 'q':
            print("Выход из программы.")
            break

        else:
            print("Неизвестная команда. Попробуйте снова.")

if __name__ == '__main__':
    main()