import logging
import sys
import asyncio

from handlers import dp
from init import log_error, bot, set_main_menu
from config import Config
from utils.local_data_utils import check_data_files_on_start


async def main() -> None:
    check_data_files_on_start()
    await set_main_menu()
    await dp.start_polling(bot)


if __name__ == '__main__':
    if Config.debug:
        logging.basicConfig (level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start bot', with_traceback=False)
    asyncio.run (main ())
