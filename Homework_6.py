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