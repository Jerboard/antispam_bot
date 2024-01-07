import logging
import re

from pyrogram.types import Message

from difflib import SequenceMatcher
from datetime import datetime

import db
from init import bot, only_group_filter, ARABIC_PATTERN, log_error
from utils.message_utils import get_full_name, check_entities


async def delete_scam_message(msg: Message, time_start: datetime):
    await msg.delete()

    if msg.media_group_id:
        await db.add_mediagroup(chat_id=msg.chat.id, media_group_id=msg.media_group_id)

    all_chats = await db.get_all_chats()
    for chat in all_chats:
        try:
            await bot.ban_chat_member(
                chat_id=chat.chat_id,
                user_id=msg.from_user.id
            )
        except Exception as ex:
            logging.warning(f'{msg.from_user.id} {ex}')

    await db.add_action (time_start=time_start)


# арабская вязь, имя канала,
@bot.on_edited_message(only_group_filter)
@bot.on_message(only_group_filter)
async def antispam(client, msg: Message):
    # await db.init_models()
    time_start = datetime.now()
    user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
    is_anonymous_admin = False
    if msg.from_user.username == 'GroupAnonymousBot' or msg.from_user.id in [777000, 1148629068]:
        is_anonymous_admin = True

    if user.status == 'creator' or user.status == 'administrator' or is_anonymous_admin is True:
        pass
    else:
        text = msg.text if msg.text is not None else msg.caption

        user_full_name = get_full_name(msg.from_user.first_name, msg.from_user.last_name)

        arabic_name = ARABIC_PATTERN.findall (user_full_name)
        if arabic_name or msg.from_user.is_bot:
            await delete_scam_message(
                msg=msg,
                time_start=time_start)
            return

        if text:
            entities = msg.entities if msg.entities else msg.caption_entities

            # если по вложениям всё ок
            if check_entities(entities):
                await delete_scam_message (
                    msg=msg,
                    time_start=time_start)
                return

            arabic_text = ARABIC_PATTERN.findall (text)
            if arabic_text:
                await delete_scam_message (
                    msg=msg,
                    time_start=time_start)
                return

        if msg.media_group_id:
            result = await db.get_mediagroup(msg.media_group_id)
            if result:
                await msg.delete()
                return

        similarity_ratio = SequenceMatcher (None, msg.chat.title, user_full_name).ratio ()
        if similarity_ratio >= 0.85:
            await msg.delete()

    await db.add_action(time_start=time_start)
