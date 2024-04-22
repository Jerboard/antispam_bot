from aiogram.types import MessageEntity
from aiogram.enums.message_entity_type import MessageEntityType

from init import log_error


def get_full_name(first_name, last_name):
    return f'{first_name} {last_name}'.replace('None', '').strip()


# проверяет сущности
def check_entities(entities: list[MessageEntity]) -> bool:
    delete_message = False
    source = None
    if entities:
        for entity in entities:
            print (type (entity.type), entity.type)
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
