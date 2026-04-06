import asyncio
from telethon import TelegramClient

from settings import conf


async def main():
    async with TelegramClient(
            conf.session_name,
            conf.api_id,
            conf.api_hash
    ) as client:
        await client.start(phone=conf.phone)
        print("✅ Сессия создана")
        print(f"Файл: {conf.session_name}.session")


if __name__ == "__main__":
    asyncio.run(main())
