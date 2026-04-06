import asyncio
import logging
import os

from telethon import TelegramClient, events


from settings import conf

# API_ID = int(os.environ["TG_API_ID"])
# API_HASH = os.environ["TG_API_HASH"]
# SESSION = os.environ.get("TG_SESSION", "")


log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

client = TelegramClient(conf.session_name, conf.api_id, conf.api_hash)


@client.on(events.NewMessage(pattern="/start"))
async def handler(event):
    await event.reply("Bot connected!")


async def main():
    await client.connect()
    # if not await client.is_user_authorized():
    #     # здесь Telethon запросит код
    #     code = input("Code: ")
    #     await client.sign_in(code=code)

    print("Авторизован, запускаем обработчики…")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
