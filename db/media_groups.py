import sqlalchemy as sa
import typing as t

from datetime import date, datetime

from db.base import METADATA, begin_connection


class MediaGroupRow(t.Protocol):
    id: int
    chat_id: int
    media_group_id: int


MediaGroupTable = sa.Table(
    'mediagroup',
    METADATA,
    sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
    sa.Column('chat_id', sa.BigInteger),
    sa.Column('media_group_id', sa.BigInteger),
)


# добавляет медиагруппу
async def add_mediagroup(chat_id: int, media_group_id: int):
    async with begin_connection() as conn:
        result = await conn.execute(
            MediaGroupTable.select ().where (MediaGroupTable.c.chat_id == chat_id)
        )
        result = result.first()
        if result is None:
            await conn.execute(
                MediaGroupTable.insert().values(
                    chat_id=chat_id,
                    media_group_id=media_group_id
                )
            )

        else:
            await conn.execute(
                MediaGroupTable.update().where(MediaGroupTable.c.chat_id == chat_id).values(media_group_id=media_group_id)
            )


# возвращает медиагруппу
async def get_mediagroup(media_group_id: int):
    async with begin_connection () as conn:
        result = await conn.execute(
            MediaGroupTable.select().where(MediaGroupTable.c.media_group_id == media_group_id)
        )
    return result.first()
