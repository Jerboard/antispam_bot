from aiogram.types import MessageEntity
from aiogram.enums.message_entity_type import MessageEntityType

import keyboards as kb
from config import Config
from init import log_error, bot
from utils import local_data_utils as dt
from enums import lists_ex, ListEx


async def get_admin_start_screen(user_id: int, message_id: int = None):
    wl_users = dt.get_white_list (lists_ex[ListEx.WL_USERS.value])
    wl_url = dt.get_white_list (lists_ex [ListEx.WL_URL.value])
    wl_phrase = dt.get_white_list (lists_ex[ListEx.WL_PHRASE.value])
    bl_phrase = dt.get_white_list (lists_ex[ListEx.BL_PHRASE.value])

    if wl_users:
        wl_users_text = f'<b>⚪️ Белый список пользователей:</b>\n' + "\n".join(wl_users)
    else:
        wl_users_text = '<b>⚪️ Белый список пользователей пуст</b>'

    if wl_phrase:
        wl_phrase_text = f'<b>⚪️ Белый список фраз:</b>\n' + "\n".join(wl_phrase)
    else:
        wl_phrase_text = '<b>⚪️ Белый список фраз пуст</b>'

    if wl_url:
        wl_url_text = f'<b>⚪️ Белый список ссылок:</b>\n' + "\n".join(wl_url)
    else:
        wl_url_text = '<b>⚪️ Белый список ссылок пуст</b>'

    if bl_phrase:
        bl_phrase_text = f'<b>⚫️ Чёрный список фраз:</b>\n' + "\n".join(bl_phrase)
    else:
        bl_phrase_text = '<b>⚫️ Чёрный список фраз пуст</b>'

    text = (f'{wl_users_text}\n\n'
            f'{wl_url_text}\n\n'
            f'{wl_phrase_text}\n\n'
            f'{bl_phrase_text}\n\n'
            )

    if message_id:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=text,
            disable_web_page_preview=True,
            reply_markup=kb.get_main_kb ()
        )
    else:
        await bot.send_message (
            chat_id=user_id,
            text=text,
            disable_web_page_preview=True,
            reply_markup=kb.get_main_kb ()
        )


# проверяет сущности
def check_entities(entities: list[MessageEntity]) -> bool:
    delete_message = False
    source = None
    if entities:
        for entity in entities:
            if entity.type == MessageEntityType.TEXT_LINK:
                delete_message = True
                source = 'TEXT_LINK'
                break
            elif entity.type == MessageEntityType.URL:
                delete_message = True
                source = 'URL'
                break
            elif entity.type == MessageEntityType.CODE:
                delete_message = True
                source = 'CODE'
                break
            elif entity.type == MessageEntityType.MENTION:
                delete_message = True
                source = 'MENTION'
                break

    if delete_message:
        log_error(f'del entities {source}', with_traceback=False)

    return delete_message
