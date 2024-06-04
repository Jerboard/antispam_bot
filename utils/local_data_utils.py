import os
import json
import re

from config import Config
from enums import lists_ex


# проверка наличия файлов при запуске
def check_data_files_on_start():
    data_file_path = os.path.join (Config.data_path)
    if not os.path.exists (data_file_path):
        os.makedirs (data_file_path)

    for k, v in lists_ex.items():
        data_file_path = os.path.join (Config.data_path, v)
        if not os.path.exists (data_file_path):
            data = []
            with open (data_file_path, 'w') as file:
                json.dump (data, file)


# Возвращает вайтлист
def get_white_list(filename: str) -> list:
    data_file_path = os.path.join (Config.data_path, filename)
    with open (data_file_path, 'r') as file:
        data: list = json.load (file)
    return data


# Добавляет в вайтлист
def add_in_white_list(new_data: str | int, filename: str):
    data_file_path = os.path.join(Config.data_path, filename)
    with open (data_file_path, 'r') as file:
        data: list = json.load (file)

    data.append(new_data)
    with open (data_file_path, 'w') as file:
        json.dump (data, file)


# Удаляет из вайтлиста
def del_from_white_list(index_el: int, filename: str):
    data_file_path = os.path.join(Config.data_path, filename)
    with open (data_file_path, 'r') as file:
        data: list = json.load (file)

    # data.remove(index_el)
    del_el = data.pop(index_el)
    with open (data_file_path, 'w') as file:
        json.dump (data, file)
    return del_el


# проверяет есть ли элемент в списке в списке
def check_text_list(text: str, list_ex: str) -> bool:
    list_ = get_white_list (f'{list_ex}.json')
    result = False

    for el in list_:
        pattern = re.escape(el).replace(r'\*', '.*')
        match = re.search (pattern, text, re.IGNORECASE)
        if match:
            result = True
            break
    return result