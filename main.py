import logging
import sys

from handlers import bot
from init import DEBUG


if __name__ == '__main__':
    if DEBUG:
        logging.basicConfig (level=logging.INFO, stream=sys.stdout)
    else:
        logging.basicConfig (level=logging.WARNING, filename='log.log')
    bot.run ()
