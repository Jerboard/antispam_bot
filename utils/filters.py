from pyrogram.enums.chat_type import ChatType


async def group_filter(_, __, query):
    return query.chat.type != ChatType.PRIVATE
