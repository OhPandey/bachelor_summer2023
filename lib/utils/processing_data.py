import re
from datetime import datetime

blacklist = [
    "Nom", "Name", "Prenom", "Born", "Matricule", "le", "Bom", "|", "Neve", "", "/"
]

student_dic: dict = {
    'last_name': str(),
    'first_name': str(),
    'birth_day': int(),
    'birth_month': str(),
    'birth_year': int(),
    'student_id': int()
}


def is_student_dic_empty(value: dict):
    if value["last_name"] is str():
        return True

    if value["first_name"] is str():
        return True

    if value["birth_day"] is int():
        return True

    if value["birth_month"] is str():
        return True

    if value["birth_year"] is int():
        return True

    if value["student_id"] is int():
        return True

    return False


def is_student_id(value):
    match = re.search(r"\d{10}", value)
    if match:
        return match.group()

    return int()


def is_year(value):
    match = re.search(r"\d{4}", value)
    if match:
        if 1900 <= int(match.group()) < datetime.now().year:
            return match.group()

    return int()


def is_month(value):
    match = re.search(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b",
                      value, re.IGNORECASE)
    if match:
        return match.group()

    return str()


def is_day(value):
    match = re.search(r"\d{2}", value)
    if match:
        if 0 < int(match.group()) <= 31:
            return match.group()

    return int()


def processing_data_easyocr(data_list: list):
    # Split every element in the list
    array = list()
    for element in data_list:
        split_values = element.split()
        array.extend(split_values)

    return processing_data(array)


def processing_data_tesseract(data_list: list):
    return processing_data(data_list)


def processing_data(data_list: list):
    # Copy dictionary (call by reference)
    data = student_dic.copy()

    for element in data_list:
        if element in blacklist:
            continue

        result = is_student_id(element)
        if result is not int():
            data["student_id"] = result
            continue

        result = is_year(element)
        if result is not int():
            data["birth_year"] = result
            continue

        result = is_month(element)
        if result is not str():
            data["birth_month"] = result
            continue

        result = is_day(element)
        if result is not int():
            data["birth_day"] = result
            continue

        if element.isupper():
            data["last_name"] += " " + element
        else:
            data["first_name"] += " " + element

    if data["last_name"] is not str():
        if data["last_name"][0] == " ":
            data["last_name"] = data["last_name"][1:]

    if data["first_name"] is not str():
        if data["first_name"][0] == " ":
            data["first_name"] = data["first_name"][1:]

    print(data)

    if is_student_dic_empty(data):
        return None

    return data
