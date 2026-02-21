from datetime import datetime

newspapers = [
    {
        "name": "The Moscow Times",
        "date": "Wednesday, October 2, 2002",
        "format": "%A, %B %d, %Y"
    },
    {
        "name": "The Guardian",
        "date": "Friday, 11.10.13",
        "format": "%A, %d.%m.%y"
    },
    {
        "name": "Daily News",
        "date": "Thursday, 18 August 1977",
        "format": "%A, %d %B %Y"
    }
]

for paper in newspapers:
    try:
        date_object = datetime.strptime(paper["date"], paper["format"])
        print(f"{paper['name']}: {date_object}")
    except ValueError:
        print(f"{paper['name']}: Неверный формат даты")
