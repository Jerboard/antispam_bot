import logging

from handlers import bot


if __name__ == '__main__':
    logging.basicConfig (level=logging.WARNING, filename='log.log')
    print('start')
    bot.run ()