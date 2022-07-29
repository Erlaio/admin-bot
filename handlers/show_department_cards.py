from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default.keyboards import DepartmentsKeyboard
from loader import dp, bot
from pkg.db.user_func import get_users_from_department_name
from states.show_user_state import UserCardState
from utils.check_is_available import is_department_available
from utils.send_card import send_card


@dp.message_handler(commands="show_department_cards")
async def show_user_by_department_start(message: types.Message):
    text = 'Выберите отдел для вывода'
    await message.answer(text, reply_markup=await DepartmentsKeyboard.get_reply_keyboard())
    await UserCardState.show_departments.set()


@dp.message_handler(state=UserCardState.show_departments)
async def show_users_by_department(message: types.Message, state: FSMContext):
    department_name = message.text
    if await is_department_available(department_name):
        data = await get_users_from_department_name(department_name=department_name)
        if not data:
            await bot.send_message(message.chat.id, 'Никто не привязан к отделу',
                                   reply_markup=ReplyKeyboardRemove())
        for user in data:
            await send_card(message, user)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Такой отдел не найден.',
                               reply_markup=ReplyKeyboardRemove())
        await state.finish()
