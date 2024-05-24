from aiogram.types import Message
from aiogram.enums.chat_member_status import ChatMemberStatus

from difflib import SequenceMatcher
from datetime import datetime

import db
from init import dp, bot, log_error
from config import Config
from utils.message_utils import check_entities
from utils import local_data_utils as dt


async def delete_scam_message(msg: Message, time_start: datetime):
    await msg.delete()
    log_error(f'Удалил сообщение', with_traceback=False)

    if msg.media_group_id:
        await db.add_mediagroup(chat_id=msg.chat.id, media_group_id=int(msg.media_group_id))

    log_error (
        f'Баню пользователя: '
        f'{msg.from_user.id, msg.from_user.full_name, msg.from_user.username}\n'
        f'В чате {msg.chat.title}\n'
        f'Текст: {msg.text}', with_traceback=False)
    try:
        await bot.ban_chat_member(
            chat_id=msg.chat.id,
            user_id=msg.from_user.id
        )
    except Exception as ex:
        log_error(ex)

    await db.add_action (time_start=time_start)


# арабская вязь, имя канала,
@dp.message(lambda msg: msg.chat.type == 'supergroup' or msg.chat.type == 'group')
@dp.edited_message(lambda msg: msg.chat.type == 'supergroup' or msg.chat.type == 'group')
async def antispam(msg: Message):
    time_start = datetime.now()
    white_list = dt.get_white_list ()
    is_admin = False

    if msg.from_user.username == 'GroupAnonymousBot' or msg.from_user.id == 777000:
        is_admin = True

    elif msg.from_user.id in white_list or msg.from_user.username in white_list:
        is_admin = True

    else:
        try:
            user = await bot.get_chat_member(msg.chat.id, msg.from_user.id)
            if user.status == ChatMemberStatus.CREATOR or user.status == ChatMemberStatus.ADMINISTRATOR:
                is_admin = True
        except:
            pass

    # is_admin = False
    if is_admin:
        pass
    else:
        text = msg.text if msg.text is not None else msg.caption

        if text:
            entities = msg.entities if msg.entities else msg.caption_entities

            # если по вложениям всё ок
            if check_entities(entities):
                await delete_scam_message (
                    msg=msg,
                    time_start=time_start)
                return

            # arabic_text = Config.arabic_pattern.findall (text)

        if msg.media_group_id:
            result = await db.get_mediagroup(int(msg.media_group_id))
            if result:
                await msg.delete()
                return

        similarity_ratio = SequenceMatcher (
            None,
            msg.chat.title.replace(' ', ''),
            msg.from_user.full_name.replace(' ', '').replace('_', '')
        ).ratio ()
        if similarity_ratio >= 0.8:
            log_error (f'del ratio\n{msg.chat.title} == {msg.from_user.full_name}')
            await delete_scam_message (
                msg=msg,
                time_start=time_start)

    await db.add_action(time_start=time_start)
