from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from pkg.db.models.user import User
from loader import bot


async def send_card(message: types.Message, user: User) -> None:
    caption = f'ФИО: {user.surname} {user.name} {user.patronymic}\n' \
              f'Пол: {user.gender}\n' \
              f'Логин в Telegram: {user.tg_login}\n' \
              f'Желаемый отдел: {user.desired_department}\n' \
              f'Скилы: {user.skills}\n' \
              f'Цели: {user.goals}\n' \
              f'Описание лида: {user.lead_description}\n' \
              f'Время присоединения: {user.join_time}\n'
    if user.is_approved == 1:
        caption += 'Анкета проверена\n'
    if user.is_moderator == 1:
        caption += 'Модератор\n'
    try:
        await bot.send_photo(message.chat.id, user.photo, caption=caption,
                             reply_markup=ReplyKeyboardRemove())
    except BadRequest:
        await message.answer(caption + '\nФото отсутствует в бд',
                             reply_markup=ReplyKeyboardRemove())
