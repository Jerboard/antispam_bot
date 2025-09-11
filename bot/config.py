from os import getenv

import re


class Config:
    debug = getenv ('DEBUG') == '1'
    # debug = getenv ('DEBUG') == '0'
    # if debug:
    #     token = getenv ('TOKEN_TEST')
    # else:
    #     token = getenv ('TOKEN')

    token = getenv('TOKEN')

    db_host = getenv('DB_HOST')
    db_port = getenv('DB_PORT')
    db_name = getenv('POSTGRES_DB')
    db_user = getenv('POSTGRES_USER')
    db_password = getenv('POSTGRES_PASSWORD')
    db_url = f'postgresql+asyncpg://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    redis_host = getenv('REDIS_HOST')
    redis_port = int(getenv('REDIS_PORT'))

    # tz = timezone ('Europe/Moscow')
    # my_id = int (getenv ('MY_ID'))

    api_id = getenv ('API_ID')
    api_hash = getenv ('API_HAS')

    arabic_pattern = re.compile (r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    admins = [524275902, 1456925942, 650850638]

    data_path = 'data'
    wl_filename = 'white_list.json'
