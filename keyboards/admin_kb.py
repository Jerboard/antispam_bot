from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from enums import AdminCB, ListEx


# # главная клавиатура
def get_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='➕ БС пользователей', callback_data=f'{AdminCB.ADD_WL.value}:{ListEx.WL_USERS.value}')
    kb.button(text='➖ БС пользователей', callback_data=f'{AdminCB.DEL_WL.value}:{ListEx.WL_USERS.value}')
    kb.button(text='➕ БС ссылок', callback_data=f'{AdminCB.ADD_WL.value}:{ListEx.WL_URL.value}')
    kb.button(text='➖ БС ссылок', callback_data=f'{AdminCB.DEL_WL.value}:{ListEx.WL_URL.value}')
    kb.button(text='➕ БС хештегов и юзернеймов', callback_data=f'{AdminCB.ADD_WL.value}:{ListEx.WL_PHRASE.value}')
    kb.button(text='➖ БС хештегов и юзернеймов', callback_data=f'{AdminCB.DEL_WL.value}:{ListEx.WL_PHRASE.value}')
    kb.button(text='➕ ЧС фраз', callback_data=f'{AdminCB.ADD_WL.value}:{ListEx.BL_PHRASE.value}')
    kb.button(text='➖ ЧС фраз', callback_data=f'{AdminCB.DEL_WL.value}:{ListEx.BL_PHRASE.value}')
    return kb.adjust(2).as_markup()


# главная клавиатура
# def get_main_kb() -> InlineKeyboardMarkup:
#     kb = InlineKeyboardBuilder()
#     kb.button(text='➕ WL users', callback_data=f'{AdminCB.ADD_WL.value}:{ListEx.WL_USERS.value}')
#     kb.button(text='➖ WL users', callback_data=f'{AdminCB.DEL_WL.value}:{ListEx.WL_USERS.value}')
#     kb.button(text='➕ WL url', callback_data=f'{AdminCB.ADD_WL.value}:{ListEx.WL_URL.value}')
#     kb.button(text='➖ WL url', callback_data=f'{AdminCB.DEL_WL.value}:{ListEx.WL_URL.value}')
#     kb.button(text='➕ WL phrase', callback_data=f'{AdminCB.ADD_WL.value}:{ListEx.WL_PHRASE.value}')
#     kb.button(text='➖ WL phrase', callback_data=f'{AdminCB.DEL_WL.value}:{ListEx.WL_PHRASE.value}')
#     kb.button(text='➕ BL phrase', callback_data=f'{AdminCB.ADD_WL.value}:{ListEx.BL_PHRASE.value}')
#     kb.button(text='➖ BL phrase', callback_data=f'{AdminCB.DEL_WL.value}:{ListEx.BL_PHRASE.value}')
#     return kb.adjust(2).as_markup()


# назад на главный экран
def get_back_com_start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=f'{AdminCB.BACK_MAIN.value}')
    return kb.adjust(1).as_markup()


# удаляет пользователя
def get_del_user_wl_kb(wl: list, list_ex) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    i = 0
    for user in wl:
        kb.button (text=f'🗑 {user}', callback_data=f'{AdminCB.DEL_USER_WL.value}:{i}:{list_ex}')
        i += 1
    kb.button(text='🔙 Назад', callback_data=f'{AdminCB.BACK_MAIN.value}')
    return kb.adjust(1).as_markup()
