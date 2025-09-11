import sqlalchemy as sa
import typing as t

from db.base import METADATA, begin_connection


class ChatRow(t.Protocol):
    id: int
    chat_id: int
    chat_title: str


ChatTable = sa.Table(
    'chats',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('chat_id', sa.BigInteger),
    sa.Column('chat_title', sa.String(255)),
)


# добавляет чат
async def add_chat(chat_id: int, chat_title: str):
    async with begin_connection() as conn:
        result = await conn.execute(
            ChatTable.select ().where (ChatTable.c.chat_id == chat_id)
        )
        result = result.first()
        if not result:
            await conn.execute(
                ChatTable.insert().values(
                    chat_id=chat_id,
                    chat_title=chat_title
                )
            )


# все чаты списком
async def get_all_chats() -> tuple[ChatRow]:
    async with begin_connection() as conn:
        result = await conn.execute(
            ChatTable.select()
        )

    return result.all()

