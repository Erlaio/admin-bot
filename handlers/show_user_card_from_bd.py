from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from keyboard.default.show_user_button import show_user
from loader import dp, bot
from pkg.db.user_func import get_user_by_id, get_all_users
from states.show_user_state import UserCardState


@dp.message_handler(commands="show_card")
async def show_user_start(message: types.Message):
    text = 'Вы хотите посмотреть всех пользователей или кого-то конкретного?'
    await message.answer(text, reply_markup=show_user)
    await UserCardState.show_user_choice.set()


@dp.message_handler(state=UserCardState.show_user_choice)
async def show_user_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Посмотреть всех':
        user_list = get_all_users()
        if user_list:
            for i_user in user_list:
                await message.answer(f'Имя: {i_user.name},\n'
                                     f'Фамилия: {i_user.surname},\n'
                                     f'Отчество: {i_user.patronymic},\n'
                                     f'Пол: {i_user.gender},\n'
                                     f'Почта: {i_user.email},\n'
                                     f'Ссылка на Git: {i_user.git},\n'
                                     f'Логин в Telegram: {i_user.tg_login},\n'
                                     f'Желаемый отдел: {i_user.desired_department},\n'
                                     f'Скилы: {i_user.skills},\n'
                                     f'Цели: {i_user.goals},\n'
                                     f'Описание лида: {i_user.lead_description},\n'
                                     f'Время присоединения: {i_user.join_time},\n'
                                     f'Является модератором: {i_user.is_moderator},\n'
                                     f'Принят: {i_user.is_approved},\n', reply_markup=ReplyKeyboardRemove()
                                     )
                try:
                    await bot.send_photo(message.chat.id, i_user.photo)
                except BadRequest:
                    await message.answer('Фото отсутствует в бд')
            await state.finish()
        else:
            await message.answer('Пользователи отсутствуют')
            await state.finish()

    elif answer == 'Посмотреть конкретного':
        await message.answer('Введите id', reply_markup=ReplyKeyboardRemove())
        await UserCardState.user_id.set()


@dp.message_handler(state=UserCardState.user_id)
async def show_user_by_id(message: types.Message, state: FSMContext):
    user_id = message.text

    try:
        user = get_user_by_id(int(user_id))
        await message.answer(f'Имя: {user.name},\n'
                             f'Фамилия: {user.surname},\n'
                             f'Отчество: {user.patronymic},\n'
                             f'Пол: {user.gender},\n'
                             f'Почта: {user.email},\n'
                             f'Ссылка на Git: {user.git},\n'
                             f'Логин в Telegram: {user.tg_login},\n'
                             f'Желаемый отдел: {user.desired_department},\n'
                             f'Скилы: {user.skills},\n'
                             f'Цели: {user.goals},\n'
                             f'Описание лида: {user.lead_description},\n'
                             f'Время присоединения: {user.join_time},\n'
                             f'Является модератором: {user.is_moderator},\n'
                             f'Принят: {user.is_approved},\n', reply_markup=ReplyKeyboardRemove()
                             )
        try:
            await bot.send_photo(message.chat.id, user.photo)
        except BadRequest:
            await message.answer('Фото отсутствует в бд')
    except TypeError:
        await message.answer('Пользователь с таким id не найден.', reply_markup=show_user)
        await UserCardState.show_user_choice.set()
    except ValueError:
        await message.answer('Введите id в числовом формате.')
        await UserCardState.user_id.set()
    else:
        await state.finish()
