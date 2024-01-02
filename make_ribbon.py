import openpyxl
import json
import os

cwd = os.getcwd()
print(cwd)

def make_ribbon_dict():
    ################## создание словаря RIBBON ##################
    ribbon_path = f"{cwd}/data/ribbon.xlsx"
    ribbon_dict = dict()
    ribbon_book = openpyxl.load_workbook(filename=ribbon_path)
    for sheet in ribbon_book.worksheets:
        bs_count = 0
        for i in range(5, sheet.max_row):
            if sheet[f'a{i}'].value != None:
                bs = sheet[f'a{i}'].value[:8].replace("00", "", 1)#
                ribbon_dict[bs] = {
                    "id": bs_count,
                    "address": sheet[f'c{i}'].value.strip("\\").replace("\\"," "),
                    "latitude": sheet[f'e{i}'].value,
                    "longitude": sheet[f'd{i}'].value,
                    "cunstruction": sheet[f'f{i}'].value,
                    "responcible": sheet[f'l{i}'].value,
                    "coordinates": str(sheet[f'e{i}'].value) + " " + str(sheet[f'd{i}'].value),
                    "yandex_map": f"https://yandex.ru/navi/?whatshere%5Bzoom%5D=17&whatshere%5Bpoint%5D={sheet[f'd{i}'].value}%2C{sheet[f'e{i}'].value}"}
            bs_count += 1
    with open("ribbon_RDB_dummy.py","w",encoding="utf-8") as file:
        json.dump(ribbon_dict,file,indent=4,ensure_ascii=False)
make_ribbon_dict()