import logging
import sys
import asyncio

from handlers import dp
from init import DEBUG, log_error, bot


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig (level=logging.INFO, stream=sys.stdout)
    else:
        log_error('start bot', with_traceback=False)
    asyncio.run (main ())
