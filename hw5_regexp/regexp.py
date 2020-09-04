import csv
import re
from typing import Tuple


def get_full_name(lastname: str, firstname: str, surname) -> Tuple[str, str, str]:
    name_pattern = re.compile(r'^(?P<lastname>\w+)\s?(?P<firstname>\w+)\s?(|(?P<surname>\w+))\s*$')
    # собираем фамилию имя и отчество в строку:
    full_name = ' '.join([lastname, firstname, surname])
    matched_name = name_pattern.match(full_name).groupdict()
    # выделяем группы, необходимые для форматирования ФИО:
    lastname = matched_name['lastname']
    firstname = matched_name['firstname']
    surname = matched_name['surname']

    return lastname, firstname, surname or ''


def get_phones(phone: str) -> str:
    phone_pattern = re.compile(r'^(?P<country>[+7|8]+)\s?[(]?'
                               r'(?P<code>\d{3})[/)|-]?\s?'
                               r'(?P<group1>\d{3})[-]?'
                               r'(?P<group2>\d{2})[-]?'
                               r'(?P<group3>\d{2})\s?[(]?'
                               r'(?P<add>\w{3}\.)?\s?'
                               r'(?P<add_code>\d{4})?[/)]?$'
                               )

    if phone:
        matched_phone = phone_pattern.match(phone).groupdict()
        # выделяем группы, необходимые для форматирования номера:
        code = matched_phone['code']
        group1 = matched_phone['group1']
        group2 = matched_phone['group2']
        group3 = matched_phone['group3']
        add = matched_phone['add']
        add_code = matched_phone['add_code']
        # проверка на наличие добавочного номера:
        if add:
            # формируем из групп строку с номером по формату:
            return f'+7({code}){group1}-{group2}-{group3} {add}{add_code}'
        else:
            return f'+7({code}){group1}-{group2}-{group3}'
    else:
        # если телефон не указан возвращаем пустую строку:
        return ''


def fix_contacts() -> list:
    """
    с помощью функций get_full_name и get_phones форматирует поля с ФОИ и номера телефонов
    """
    result = []
    for contact in contacts_list:
        lastname, firstname, surname = get_full_name(contact['lastname'],
                                                     contact['firstname'],
                                                     contact['surname']
                                                     )
        phone = get_phones(contact['phone'])
        result.append({**contact,
                       'lastname': lastname,
                       'firstname': firstname,
                       'surname': surname,
                       'phone': phone}
                      )
    return result


def merge_duplicates(contacts: list) -> dict:
    """
    принимает на вход результат функции fix_contacts и мёрджит дублирующиеся строки:
    """
    result = {}
    for person in contacts:
        # формируем структуру словаря merged_contacts:
        # ключом будет кортеж (имя, фамилия), значением - список всех остальных полей
        person_key = (person['lastname'], person['firstname'])
        person_values = [person['surname'],
                         person['organization'],
                         person['position'],
                         person['phone'],
                         person['email']
                         ]
        # если в merged_contacts уже есть текущий ключ - итерируемся по списку его значений
        # и мёрджим недостающие поля
        if person_key in result:
            for i in range(len(person_values)):
                if not result[person_key][i] and person_values[i]:
                    result[person_key][i] = person_values[i]
        else:
            result.update({person_key: person_values})
    return result


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.DictReader(f, delimiter=",")
        contacts_list = list(rows)

    fixed_contacts = fix_contacts()
    merged_contacts = merge_duplicates(fixed_contacts)

    # заголовки для записи в csv:
    headers = list(contacts_list[0].keys())

    fixed_contacts_list = list()
    fixed_contacts_list.append(headers)

    for k, v in merged_contacts.items():
        x = list(k) + list(v)
        fixed_contacts_list.append(x)

    with open("fixed_phonebook.csv", "w", encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(fixed_contacts_list)
