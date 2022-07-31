from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default.pagination import Pagination, InlineKeyboardButton
from keyboard.default.show_user_keyboard import ShowUserKeyboard
from loader import dp, bot
from pkg.db.user_func import get_user_by_id, get_all_users, get_user_by_tg_login
from states.show_user_state import UserCardState
from utils.send_card import send_card


@dp.message_handler(commands="show_card")
async def show_user_start(message: types.Message):
    text = 'Вы хотите посмотреть всех пользователей или кого-то конкретного?'
    await message.answer(text, reply_markup=ShowUserKeyboard.KEYBOARD)
    await UserCardState.show_user_choice.set()


@dp.message_handler(state=UserCardState.show_user_choice)
async def show_user_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Посмотреть всех':
        await message.answer('Постраничный вывод всех пользователей', reply_markup=ReplyKeyboardRemove())
        await show_all(message, state)

    elif answer == 'Посмотреть по ID':
        await message.answer('Введите id', reply_markup=ReplyKeyboardRemove())
        await UserCardState.user_id.set()

    elif answer == 'Посмотреть по Логину в Telegram':
        await message.answer('Введите логин Telegram', reply_markup=ReplyKeyboardRemove())
        await UserCardState.user_tg_login.set()


@dp.message_handler(state=UserCardState.user_id)
async def show_user_by_id(message: types.Message, state: FSMContext):
    user_id = message.text
    try:
        user = get_user_by_id(int(user_id))
        await send_card(message, user)
    except TypeError:
        await message.answer('Пользователь с таким id не найден.',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()
    except ValueError:
        await message.answer('Введите id в числовом формате.')
        await UserCardState.user_id.set()
    else:
        await state.finish()


@dp.message_handler(state=UserCardState.user_tg_login)
async def show_user_by_tg_login(message: types.Message, state: FSMContext):
    user_tg_login = message.text
    try:
        user = get_user_by_tg_login(user_tg_login)
        await send_card(message, user)
    except TypeError:
        await message.answer('Пользователь с таким логином не найден.',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await state.finish()
