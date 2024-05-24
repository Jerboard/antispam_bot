from dotenv import load_dotenv
from os import getenv
from pytz import timezone

import re


load_dotenv ()

DEBUG = bool (int (getenv ('DEBUG')))


class Config:
    if DEBUG:
        token = getenv ('TOKEN_TEST')
    else:
        token = getenv ('TOKEN')
    db_url = getenv('DB_URL')

    tz = timezone ('Europe/Moscow')

    arabic_pattern = re.compile (r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')
    admins = [524275902, 1456925942, 650850638]

    data_path = 'data'

    @staticmethod
    def debug(self):
        return DEBUG
