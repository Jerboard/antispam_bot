import logging

from pyrogram.types import MessageEntity
from pyrogram.enums import MessageEntityType


def get_full_name(first_name, last_name):
    return f'{first_name} {last_name}'.replace('None', '').strip()


# проверяет сущности
def check_entities(entities: list[MessageEntity]) -> bool:
    delete_message = False
    source = None
    if entities:
        for entity in entities:
            # print (type (entity.type), entity.type)
            if entity.type == MessageEntityType.TEXT_LINK:
                delete_message = True
                source = 'TEXT_LINK'
                break
            elif entity.type == MessageEntityType.URL:
                delete_message = True
                source = 'URL'
                break
            # elif entity.type == MessageEntityType.HASHTAG:
            #     delete_message = True
            #     source = 'HASHTAG'
            #     break
            elif entity.type == MessageEntityType.MENTION:
                delete_message = True
                source = 'MENTION'
                break

    if delete_message:
        logging.warning(f'del entities {source}')

    return delete_message
