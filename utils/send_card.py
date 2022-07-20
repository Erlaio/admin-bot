from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from loader import bot


async def send_card(message, user):
    caption = f'ФИО: {user.surname} {user.name} {user.patronymic}\n' \
              f'Пол: {user.gender}\n' \
              f'Логин в Telegram: {user.tg_login}\n' \
              f'Желаемый отдел: {user.desired_department}\n' \
              f'Скилы: {user.skills}\n' \
              f'Цели: {user.goals}\n' \
              f'Описание лида: {user.lead_description}\n' \
              f'Время присоединения: {user.join_time}\n' \
              f'Принят: {user.is_approved}\n'  # Обсудить вывод
    if user.is_moderator == 1:
        caption += 'Является модератором: Модератор\n'
    try:
        await bot.send_photo(message.chat.id, user.photo, caption=caption,
                             reply_markup=ReplyKeyboardRemove())
    except BadRequest:
        await message.answer(caption + '\nФото отсутствует в бд',
                             reply_markup=ReplyKeyboardRemove())
