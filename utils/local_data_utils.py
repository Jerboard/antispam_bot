import os
import json

import typing as t

from config import Config


# проверка наличия файлов при запуске
def check_data_files_on_start():
    data_file_path = os.path.join (Config.data_path)
    if not os.path.exists (data_file_path):
        os.makedirs (data_file_path)

    data_file_path = os.path.join (Config.data_path, Config.wl_filename)
    if not os.path.exists (data_file_path):
        data = []
        with open (data_file_path, 'w') as file:
            json.dump (data, file)


# Возвращает вайтлист
def get_white_list() -> list:
    data_file_path = os.path.join (Config.data_path, Config.wl_filename)
    with open (data_file_path, 'r') as file:
        data: list = json.load (file)
    return data


# Добавляет в вайтлист
def add_in_white_list(user: str | int):
    data_file_path = os.path.join(Config.data_path, Config.wl_filename)
    with open (data_file_path, 'r') as file:
        data: list = json.load (file)

    if user.isdigit():
        user = int(user)
    data.append(user)
    with open (data_file_path, 'w') as file:
        json.dump (data, file)


# Удаляет из вайтлиста
def del_from_white_list(user: str | int):
    data_file_path = os.path.join(Config.data_path, Config.wl_filename)
    with open (data_file_path, 'r') as file:
        data: list = json.load (file)

    data.remove(user)
    with open (data_file_path, 'w') as file:
        json.dump (data, file)