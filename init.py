from pyrogram import Client, filters
from sqlalchemy.ext.asyncio import create_async_engine

import logging
import traceback
import asyncio
import re

from datetime import datetime

from dotenv import load_dotenv
from os import getenv
from pytz import timezone

from utils.filters import group_filter

try:
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
except:
    pass

load_dotenv ()

DEBUG = bool(int(getenv('DEBUG')))
TZ = timezone('Europe/Moscow')
ENGINE = create_async_engine(url=getenv('DB_URL'))
MY_ID = int(getenv('MY_ID'))

API_ID = getenv('API_ID')
API_HAS = getenv('API_HAS')


only_group_filter = filters.create(group_filter)

ARABIC_PATTERN = re.compile (r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+')


def log_error(message):
    timestamp = datetime.now(TZ)
    filename = traceback.format_exc()[1]
    line_number = traceback.format_exc()[2]
    logging.error(f'{timestamp} {filename} {line_number}: {message}')


bot = Client("antispam")
# bot = Client("antispam", api_id=API_ID, api_hash=API_HAS)
#
# async def main():
#     async with bot:
#         await bot.send_message("me", "Hi there! I'm using **Pyrogram**")
#
#
# bot.run(main())
