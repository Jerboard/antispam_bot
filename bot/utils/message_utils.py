from aiogram.types import MessageEntity
from aiogram.enums.message_entity_type import MessageEntityType

import keyboards as kb
from init import log_error, bot
from utils import local_data_utils as dt


async def get_admin_start_screen(user_id: int, message_id: int = None):
    white_list = dt.get_white_list ()
    if white_list:
        white_text = '<b>Белый список:</b>\n'
        for user in white_list:
            white_text += f'{user}\n'
    else:
        white_text = '<b>Белый список пуст</b>'

    if message_id:
        await bot.edit_message_text(
            chat_id=user_id,
            message_id=message_id,
            text=white_text,
            reply_markup=kb.get_main_kb ()
        )
    else:
        await bot.send_message (chat_id=user_id, text=white_text, reply_markup=kb.get_main_kb ())


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
