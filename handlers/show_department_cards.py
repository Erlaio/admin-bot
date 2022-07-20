from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default import Keyboard
from keyboard.default.button_value import ButtonValue as button
from loader import dp, bot
from pkg.db.user_func import get_users_from_department
from states.show_user_state import UserCardState
from utils.send_card import send_card


@dp.message_handler(commands="show_department_cards")
async def show_user_by_department_start(message: types.Message):
    text = 'Выберите отдел для вывода'
    await message.answer(text, reply_markup=Keyboard.DEPARTMENTS)
    await UserCardState.show_departments.set()


@dp.message_handler(state=UserCardState.show_departments)
async def show_users_by_department(message: types.Message, state: FSMContext):
    data = None
    answer = message.text
    if answer == button.FRONTEND:
        data = get_users_from_department(1)
    elif answer == button.BACKEND:
        data = get_users_from_department(2)
    elif answer == button.ML:
        data = get_users_from_department(3)
    elif answer == button.DS:
        data = get_users_from_department(4)
    elif answer == button.DESIGN:
        data = get_users_from_department(5)
    elif answer == button.MOBILE_DEVELOPMENT:
        data = get_users_from_department(6)
    if data:
        for user in data:
            await send_card(message, user)
    else:
        await bot.send_message(message.chat.id, 'Такой отдел не найден.', reply_markup=ReplyKeyboardRemove())
    await state.finish()
