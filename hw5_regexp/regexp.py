import csv

# import re

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)


def get_full_name():
    # собираем фамилию, имя и отчество в строку и пишем в отдельный список contacts:
    full_name = [f'{contacts[0]} {contacts[1]} {contacts[2]}' for contacts in contacts_list]
    # разбиваем строки с ФИО по пробелу и получаем фамилию, имя и отчество в отдельных полях:
    full_name = list(map(lambda x: x.strip().split(' '), full_name))
    return full_name


def get_phones():
    # убираем из телефонов все спецсимолы и пишем их в отдельный список phones:
    phones = [''.join(list(filter(str.isalnum, phone[5]))) for phone in contacts_list]

    for i in range(1, len(phones)):
        # разбиваем номер телефона на группы:
        code = phones[i][1:4]
        g1 = phones[i][4:7]
        g2 = phones[i][7:9]
        g3 = phones[i][9:11]
        add = phones[i][11:14] + '.' + phones[i][14:]
        if phones[i] and 'доб' in phones[i]:
            phones[i] = f'+7({code}){g1}-{g2}-{g3} {add}'
        elif phones[i]:
            phones[i] = f'+7({code}){g1}-{g2}-{g3}'
    return phones


name = get_full_name()
phone = get_phones()
# присоединяем исправленные ФИО и номера телефонов к списку контактов и формируем fixed_contacts_list:
# fixed_contacts_list = []
# for i in range(len(contacts_list)):
#     fixed_contacts_list.append(name[i] + contacts_list[i][3:5] + [phone[i]] + [contacts_list[i][6]])
# print(*fixed_contacts_list, sep='\n')
print(*phone, sep='\n')

# код для записи файла в формате CSV
# with open("fixed_phonebook.csv", "w") as f:
#     datawriter = csv.writer(f, delimiter=',')
#     # Вместо contacts_list подставьте свой список
#     datawriter.writerows(contacts_list)
