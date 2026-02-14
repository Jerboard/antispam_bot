from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from datetime import datetime
from sqlalchemy.ext.asyncio import create_async_engine
from redis.asyncio import Redis

import logging
import traceback
import asyncio
import re
import os
import uvloop

from config import Config


asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
# loop = asyncio.get_event_loop()
# bot = Bot(
#     token=Config.token,
#     loop=loop,
#     default=DefaultBotProperties(parse_mode=ParseMode.HTML)
# )
dp = Dispatcher(storage=MemoryStorage())

bot = Bot(
    token=Config.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)


ENGINE = create_async_engine(url=Config.db_url)

redis_client = Redis(host=Config.redis_host, port=Config.redis_port, db=0)


async def set_main_menu():
    main_menu_commands = [
        BotCommand(command='/start', description='Главный экран'),
    ]
    await bot.set_my_commands(main_menu_commands)


def log_error(message, with_traceback: bool = True):
    now = datetime.now()
    log_folder = now.strftime ('%m-%Y')
    log_path = os.path.join('logs', log_folder)

    if not os.path.exists(log_path):
        os.makedirs(log_path)

    log_file_path = os.path.join(log_path, f'{now.day}.log')
    logging.basicConfig (level=logging.WARNING, filename=log_file_path, encoding='utf-8')
    if with_traceback:
        ex_traceback = traceback.format_exc()
        tb = ''
        msg = ''
        start_row = '  File'
        tb_split = ex_traceback.split('\n')
        for row in tb_split:
            if row.startswith(start_row) and not re.search ('venv', row):
                tb += f'{row}\n'

            if not row.startswith(' '):
                msg += f'{row}\n'

        logging.warning(f'{now}\n{tb}\n\n{msg}\n---------------------------------\n')
        return msg
    else:
        logging.warning(f'{now}\n{message}\n\n---------------------------------\n')
