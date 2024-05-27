from aiogram.types import Message
from aiogram.enums.chat_member_status import ChatMemberStatus
from aiogram.enums.message_entity_type import MessageEntityType

from difflib import SequenceMatcher
from datetime import datetime

import db
from init import dp, bot, log_error
from config import Config
from utils.message_utils import check_entities
from utils import local_data_utils as dt
from enums import lists_ex, ListEx


async def delete_scam_message(msg: Message, time_start: datetime):
    text = msg.text if msg.text is not None else msg.caption
    if dt.check_text_list(text=text, list_ex=ListEx.WL_PHRASE.value):
        return

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
    wl_users = dt.get_white_list (lists_ex[ListEx.WL_USERS.value])
    is_admin = False

    if msg.from_user.username == 'GroupAnonymousBot' or msg.from_user.id == 777000:
        is_admin = True

    elif str(msg.from_user.id) in wl_users or msg.from_user.username in wl_users:
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
            if dt.check_text_list (text=text, list_ex=ListEx.BL_PHRASE.value):
                await delete_scam_message (
                    msg=msg,
                    time_start=time_start)
                return

            entities = msg.entities if msg.entities else msg.caption_entities

            # если по вложениям всё ок
            if check_entities(entities):
                dm = True

                check_url_list = []
                for entity in entities:
                    if entity.type == MessageEntityType.TEXT_LINK:
                        check_url_list.append (entity.url)

                    elif entity.type == MessageEntityType.URL:
                        url = text[entity.offset:entity.offset + entity.length]
                        check_url_list.append(url)

                if check_url_list:
                    for url in check_url_list:
                        if not dt.check_text_list (text=url, list_ex=ListEx.WL_URL.value):
                            await delete_scam_message (
                                msg=msg,
                                time_start=time_start)
                            return

                else:
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
