import logging
import re

from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant

from difflib import SequenceMatcher
from datetime import datetime

import db
from init import bot, only_group_filter, ARABIC_PATTERN, log_error
from utils.message_utils import get_full_name, check_entities


async def delete_scam_message(msg: Message, time_start: datetime):
    await msg.delete()
    log_error(f'Удалил сообщение')

    if msg.media_group_id:
        await db.add_mediagroup(chat_id=msg.chat.id, media_group_id=msg.media_group_id)

    all_chats = await db.get_all_chats()
    for chat in all_chats:
        log_error (
            f'Баню пользователя: '
            f'{msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, msg.from_user.username}\n'
            f'в чате')
        try:
            await bot.ban_chat_member(
                chat_id=chat.chat_id,
                user_id=msg.from_user.id
            )
        except Exception as ex:
            log_error(f'{msg.from_user.id} {ex}')

    await db.add_action (time_start=time_start)


# арабская вязь, имя канала,
@bot.on_edited_message(only_group_filter)
@bot.on_message(only_group_filter)
async def antispam(client, msg: Message):
    # if msg.chat.id == -1001605611339:
    #     return
    # await db.init_models()
    await db.add_chat(chat_id=msg.chat.id, chat_title=msg.chat.title)
    time_start = datetime.now()
    is_admin = False
    if msg.from_user:
        try:
            user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
            if user.status == ChatMemberStatus.OWNER or user.status == ChatMemberStatus.ADMINISTRATOR:
                is_admin = True
        except UserNotParticipant:
            pass

    else:
        is_admin = True

    # is_admin = False
    if is_admin:
        pass
    else:
        text = msg.text if msg.text is not None else msg.caption

        user_full_name = get_full_name(msg.from_user.first_name, msg.from_user.last_name)

        arabic_name = ARABIC_PATTERN.findall (user_full_name)
        if arabic_name or msg.from_user.is_bot:
            log_error (f'\nАрабик: {user_full_name}\n')
            # await delete_scam_message(
            #     msg=msg,
            #     time_start=time_start)
            # return

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
                log_error(f'\nАрабик: {user_full_name}\n')
                # await delete_scam_message (
                #     msg=msg,
                #     time_start=time_start)
                # return

        if msg.media_group_id:
            result = await db.get_mediagroup(msg.media_group_id)
            if result:
                await msg.delete()
                return

        similarity_ratio = SequenceMatcher (
            None,
            msg.chat.title.replace(' ', ''),
            user_full_name.replace(' ', '').replace('_', '')
        ).ratio ()
        if similarity_ratio >= 0.8:
            log_error (f'del ratio\n{msg.chat.title} == {user_full_name}')
            await delete_scam_message (
                msg=msg,
                time_start=time_start)

    await db.add_action(time_start=time_start)


