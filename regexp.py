from pprint import pprint
import re
## Читаем адресную книгу в формате CSV в список contacts_list:
import csv

with open("phonebook_raw.csv", encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    # next(rows)
    contacts_list = list(rows)

final_dict = {}
# pattern = r"(\+7|8)(\s*\(?\d{3}\)?)([\s-]*\d+[\s-]*\d+[\s-]*\d+)([\s]\(?доб\)?[\s.]*\d+)*"
pattern = r"(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})"
pattern_extension_num = r"(\+7|8)(\d{3})(\d{3})(\d{2})(\d{2})(\(?доб\)?.?\d+)"
subst_pattern = r"+7(\2)-\3-\4-\5"
subst_pattern_extension_num = r"+7(\2)-\3-\4-\5 \6"
for el_list in contacts_list:
    fio_temp = el_list[0] + ' ' + el_list[1] + ' ' + el_list[2]
    fio_result = re.sub("  ", " ", fio_temp).split(' ')
    key_fi = fio_result[0] + fio_result[1]
    phone_temp = re.sub("[-| |(|)]","", el_list[5])

    if "доб" in phone_temp:
        phone = re.sub(pattern_extension_num, subst_pattern_extension_num, phone_temp)
    else:
        phone = re.sub(pattern, subst_pattern, phone_temp)

    if not key_fi in final_dict:
        final_dict[key_fi] = {'lastname': fio_result[0],
                              'firstname': fio_result[1],
                              'surname': fio_result[2],
                              'organization': el_list[3],
                              'position': el_list[4],
                              'phone': phone,
                              'email': el_list[6]}
    else:
        if fio_result[2]: final_dict[key_fi]['surname'] = fio_result[2]
        if el_list[3]: final_dict[key_fi]['organization'] = el_list[3]
        if el_list[4]: final_dict[key_fi]['position'] = el_list[4]
        if phone: final_dict[key_fi]['phone'] = phone
        if el_list[6]: final_dict[key_fi]['email'] = el_list[6]


list_final = []
for spr in final_dict.values():
    list_final.append(spr)
# pprint(list_final)
field_names = ['lastname','firstname','surname','organization','position','phone','email']
with open("phonebook.csv", "w",newline='') as f:
    datawriter = csv.DictWriter(f, fieldnames=field_names)
    datawriter.writerows(list_final)