from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

from sqlalchemy.ext.asyncio import create_async_engine

import logging
import traceback
import asyncio
import re
import os

from datetime import datetime

from dotenv import load_dotenv
from os import getenv
from pytz import timezone

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

load_dotenv ()
loop = asyncio.get_event_loop()
TOKEN = getenv('TOKEN')
bot = Bot(TOKEN, parse_mode='html')
dp = Dispatcher(loop=loop, storage=MemoryStorage())


DEBUG = bool(int(getenv('DEBUG')))
TZ = timezone('Europe/Moscow')
ENGINE = create_async_engine(url=getenv('DB_URL'))
MY_ID = int(getenv('MY_ID'))

API_ID = getenv('API_ID')
API_HAS = getenv('API_HAS')

ARABIC_PATTERN = re.compile (r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')


def log_error(message, with_traceback: bool = True):
    now = datetime.now(TZ)
    log_folder = now.strftime ('%m-%Y')
    log_path = os.path.join('logs', log_folder)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file_path = os.path.join(log_path, f'{now.day}.log')
    logging.basicConfig (level=logging.WARNING, filename=log_file_path, encoding='utf-8')
    if with_traceback:
        ex_traceback = traceback.format_exc()
        logging.warning(f'=====\n{now}\n{ex_traceback}\n{message}\n=====')
    else:
        logging.warning(f'=====\n{now}\n{message}\n=====')
