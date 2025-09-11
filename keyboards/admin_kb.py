from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup

from enums import AdminCB


# главная клавиатура
def get_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='➕ Добавить', callback_data=f'{AdminCB.ADD_WL.value}')
    kb.button(text='➖ Удалить', callback_data=f'{AdminCB.ADD_WL.value}')
    return kb.adjust(2).as_markup()


# назад на главный экран
def get_back_com_start_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text='🔙 Назад', callback_data=f'{AdminCB.BACK_MAIN.value}')
    return kb.adjust(1).as_markup()


# удаляет пользователя
def get_del_user_wl_kb(wl: list) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    for user in wl:
        kb.button (text=f'🗑 {user}', callback_data=f'{AdminCB.DEL_USER_WL.value}:{user}')
    kb.button(text='🔙 Назад', callback_data=f'{AdminCB.BACK_MAIN.value}')
    return kb.adjust(1).as_markup()
