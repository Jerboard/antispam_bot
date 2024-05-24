from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import dp
from config import Config
from utils import local_data_utils as dt
from utils.message_utils import get_admin_start_screen
from enums import AdminCB


# добавляет админа
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.ADD_WL.value))
async def add_white_list_1(cb: CallbackQuery, state: FSMContext):
    await state.set_state(AdminCB.ADD_WL)
    await state.update_data(data={'msg_id': cb.message.message_id})
    text = 'Отправьте ID или имя пользователя'
    await cb.message.edit_text(text=text, reply_markup=kb.get_back_com_start_kb())


# Добавляет пользователя
@dp.message(StateFilter(AdminCB.ADD_WL))
async def add_white_list_2(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    await state.clear()
    dt.add_in_white_list(msg.text)
    await get_admin_start_screen(user_id=msg.from_user.id, message_id=data['msg_id'])


# список на удаление
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.DEL_WL.value))
async def del_white_list_1(cb: CallbackQuery, state: FSMContext):
    white_list = dt.get_white_list ()

    text = 'Выберите пользователя для удаления'
    await cb.message.edit_text(text=text, reply_markup=kb.get_del_user_wl_kb(white_list))


# удаление пользователя
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.DEL_USER_WL.value))
async def del_white_list_1(cb: CallbackQuery, state: FSMContext):
    _, user = cb.data.split(':')

    if user.isdigit():
        user = int(user)

    dt.del_from_white_list(user)
    await cb.answer(f'❕ Пользователь {user} удалён из белого списка')

    white_list = dt.get_white_list ()

    text = 'Выберите пользователя для удаления'
    await cb.message.edit_text(text=text, reply_markup=kb.get_del_user_wl_kb(white_list))