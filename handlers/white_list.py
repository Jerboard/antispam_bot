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
    _, list_ex = cb.data.split(':')

    await state.set_state(AdminCB.ADD_WL)
    await state.update_data(data={'msg_id': cb.message.message_id, 'list_ex': list_ex})
    text = 'Отправьте новый элемент списка'
    await cb.message.edit_text(text=text, reply_markup=kb.get_back_com_start_kb())


# Добавляет пользователя
@dp.message(StateFilter(AdminCB.ADD_WL))
async def add_white_list_2(msg: Message, state: FSMContext):
    await msg.delete()
    data = await state.get_data()
    await state.clear()

    dt.add_in_white_list(new_data=msg.text, filename=f'{data["list_ex"]}.json')
    await get_admin_start_screen(user_id=msg.from_user.id, message_id=data['msg_id'])


# список на удаление
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.DEL_WL.value))
async def del_white_list_1(cb: CallbackQuery, state: FSMContext):
    _, list_ex = cb.data.split (':')
    list_ = dt.get_white_list (f'{list_ex}.json')
    if not list_:
        await cb.answer('❕ Список пуст', show_alert=True)
    else:
        text = 'Выберите элемент для удаления'
        await cb.message.edit_text(text=text, reply_markup=kb.get_del_user_wl_kb(wl=list_, list_ex=list_ex))


# удаление пользователя
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.DEL_USER_WL.value))
async def del_white_list_1(cb: CallbackQuery, state: FSMContext):
    _, index_el_str, list_ex = cb.data.split(':')
    index_el = int(index_el_str)

    filename = f'{list_ex}.json'
    del_el = dt.del_from_white_list(index_el, filename)
    await cb.answer(f'❕ Элемент {del_el} удалён из списка')

    list_ = dt.get_white_list (filename)

    text = 'Выберите пользователя для удаления'
    await cb.message.edit_text(text=text, reply_markup=kb.get_del_user_wl_kb(wl=list_, list_ex=list_ex))
