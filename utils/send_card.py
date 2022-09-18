from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from loader import bot
from pkg.db.models.user import User


async def send_card(chat_id: int, user: User, reply_markup=ReplyKeyboardRemove()) -> None:
    caption = f'ФИО: {user.surname} {user.name} {user.patronymic}\n' \
              f'Пол: {user.gender}\n' \
              f'Логин в Telegram: {user.tg_login}\n' \
              f'Желаемый отдел: {user.desired_department}\n' \
              f'Скилы: {user.skills}\n' \
              f'{user.goals}\n' \
              f'Комментарий тимлида: {user.lead_description}\n' \
              f'Время присоединения: {user.join_time}\n'
    if user.is_approved == 1:
        caption += 'Анкета проверена\n'
    if user.is_moderator == 1:
        caption += 'Модератор\n'
    try:
        await bot.send_photo(chat_id, user.photo, caption=caption,
                             reply_markup=reply_markup)
    except BadRequest:
        await bot.send_message(chat_id, caption + '\nФото отсутствует в бд',
                               reply_markup=reply_markup)
