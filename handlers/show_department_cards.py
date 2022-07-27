from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default.departments_keyboard import DepartmentsKeyboard
from loader import dp, bot
from pkg.db.user_func import get_users_from_department_name
from states.show_user_state import UserCardState
from utils.send_card import send_card


@dp.message_handler(commands="show_department_cards")
async def show_user_by_department_start(message: types.Message):
    text = 'Выберите отдел для вывода'
    await message.answer(text, reply_markup=DepartmentsKeyboard.KEYBOARD)
    await UserCardState.show_departments.set()


@dp.message_handler(state=UserCardState.show_departments)
async def show_users_by_department(message: types.Message, state: FSMContext):
    answer = message.text
    if await DepartmentsKeyboard.is_exist(answer):
        data = None
        departments = await DepartmentsKeyboard.get_departments()
        for department in departments:
            if answer == department:
                data = get_users_from_department_name(department_name=department)
        if not data:
            await bot.send_message(message.chat.id, 'Никто не привязан к отделу', reply_markup=ReplyKeyboardRemove())
            await state.finish()
        for user in data:
            await send_card(message, user)
        await state.finish()
    else:
        await bot.send_message(message.chat.id, 'Такой отдел не найден.', reply_markup=ReplyKeyboardRemove())
        await state.finish()
