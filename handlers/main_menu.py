from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

import db
import keyboards as kb
from init import dp
from config import Config
from utils import local_data_utils as dt
from utils.message_utils import get_admin_start_screen
from enums import AdminCB


# команда старт
@dp.message(CommandStart())
async def com_start(msg: Message, state: FSMContext):
    await state.clear()

    if msg.from_user.id not in Config.admins:
        return

    await get_admin_start_screen(user_id=msg.from_user.id)


# назад к команде старт
@dp.callback_query(lambda cb: cb.data.startswith(AdminCB.BACK_MAIN.value))
async def back_main_menu(cb: CallbackQuery, state: FSMContext):
    await state.clear()
    await get_admin_start_screen(user_id=cb.from_user.id, message_id=cb.message.message_id)



