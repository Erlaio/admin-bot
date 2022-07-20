from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from keyboard.default import Keyboard
from keyboard.default.button_value import ButtonValue as button
from loader import dp, bot
from pkg.db.user_func import get_user_by_id, get_all_users
from states.show_user_state import UserCardState

from pkg.db.user_func import get_users_from_department


@dp.message_handler(commands="show_card")
async def show_user_start(message: types.Message):
    text = 'Вы хотите посмотреть всех пользователей или кого-то конкретного?'
    await message.answer(text, reply_markup=Keyboard.SHOW_USER)
    await UserCardState.show_user_choice.set()


@dp.message_handler(state=UserCardState.show_user_choice)
async def show_user_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Посмотреть всех':
        user_list = get_all_users()
        if user_list:
            for i_user in user_list:
                caption = f'ФИО: {i_user.surname} {i_user.name} {i_user.patronymic}\n' \
                          f'Пол: {i_user.gender}\n' \
                          f'Логин в Telegram: {i_user.tg_login}\n' \
                          f'Желаемый отдел: {i_user.desired_department}\n' \
                          f'Скилы: {i_user.skills}\n' \
                          f'Цели: {i_user.goals}\n' \
                          f'Описание лида: {i_user.lead_description}\n' \
                          f'Время присоединения: {i_user.join_time}\n' \
                          f'Принят: {i_user.is_approved}\n'
                if i_user.is_moderator == 1:
                    caption += 'Является модератором: Модератор\n'
                try:
                    await bot.send_photo(message.chat.id, i_user.photo, caption=caption)
                except BadRequest:
                    await message.answer(caption + '\nФото отсутствует в бд', reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer('Пользователи отсутствуют')
            await state.finish()

    elif answer == 'Посмотреть конкретного':
        await message.answer('Введите id', reply_markup=ReplyKeyboardRemove())
        await UserCardState.user_id.set()

    elif answer == 'Показать всех постранично':
        user_list = get_all_users()
        if user_list:
            index = 0
            for _ in range(len(user_list) // 2):
                result = ''
                for i_user in user_list[index:index + 2]:
                    caption = f'ФИО: {i_user.surname} {i_user.name} {i_user.patronymic}\n' \
                              f'Пол: {i_user.gender}\n' \
                              f'Логин в Telegram: {i_user.tg_login}\n' \
                              f'Желаемый отдел: {i_user.desired_department}\n' \
                              f'Скилы: {i_user.skills}\n' \
                              f'Цели: {i_user.goals}\n' \
                              f'Описание лида: {i_user.lead_description}\n' \
                              f'Время присоединения: {i_user.join_time}\n' \
                              f'Принят: {i_user.is_approved}\n\n'
                    result += caption
                index += 2
                await bot.send_message(message.chat.id, result, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=UserCardState.user_id)
async def show_user_by_id(message: types.Message, state: FSMContext):
    user_id = message.text
    try:
        user = get_user_by_id(int(user_id))
        caption = f'ФИО: {user.surname} {user.name} {user.patronymic}\n' \
                  f'Пол: {user.gender}\n' \
                  f'Логин в Telegram: {user.tg_login}\n' \
                  f'Желаемый отдел: {user.desired_department}\n' \
                  f'Скилы: {user.skills}\n' \
                  f'Цели: {user.goals}\n' \
                  f'Описание лида: {user.lead_description}\n' \
                  f'Время присоединения: {user.join_time}\n' \
                  f'Принят: {user.is_approved}\n'
        if user.is_moderator == 1:
            caption += 'Является модератором: Модератор\n'
        try:
            await bot.send_photo(message.chat.id, user.photo, caption=caption)
        except BadRequest:
            await message.answer(caption + '\nФото отсутствует в бд', reply_markup=ReplyKeyboardRemove())
    except TypeError:
        await message.answer('Пользователь с таким id не найден.', reply_markup=Keyboard.SHOW_USER)
        await UserCardState.show_user_choice.set()
    except ValueError:
        await message.answer('Введите id в числовом формате.')
        await UserCardState.user_id.set()
    else:
        await state.finish()


@dp.message_handler(commands="show_department_cards")
async def show_user_by_department_start(message: types.Message, state: FSMContext):
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
            caption = f'ФИО: {user.name} {user.surname} {user.patronymic}\n' \
                      f'Пол: {user.gender}\n' \
                      f'Логин в Telegram: {user.tg_login}\n' \
                      f'Желаемый отдел: {user.desired_department}\n' \
                      f'Скилы: {user.skills}\n' \
                      f'Цели: {user.goals}\n' \
                      f'Описание лида: {user.lead_description}\n' \
                      f'Время присоединения: {user.join_time}\n' \
                      f'Принят: {user.is_approved}\n'
            if user.is_moderator == 1:
                caption += 'Является модератором: Модератор\n'
            try:
                await bot.send_photo(message.chat.id, user.photo, caption=caption)
            except BadRequest:
                await message.answer(caption + '\nФото отсутствует в бд.', reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(message.chat.id, 'Такой отдел не найден.', reply_markup=ReplyKeyboardRemove())
    await state.finish()
