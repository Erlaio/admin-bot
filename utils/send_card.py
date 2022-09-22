from aiogram.types import ReplyKeyboardRemove
from aiogram.utils.exceptions import BadRequest

from loader import bot
from pkg.db.models.user import User


async def send_card(chat_id: int, user: User, reply_markup=ReplyKeyboardRemove()) -> None:
    caption = f'<b>ФИО:</b> {user.surname} {user.name} {user.patronymic}\n' \
              f'<b>Пол:</b> {user.gender}\n' \
              f'<b>Логин в Telegram:</b> {user.tg_login}\n' \
              f'<b>Желаемый отдел:</b> {user.desired_department}\n' \
              f'<b>Скилы:</b> {user.skills}\n' \
              f'<b>Цели:</b> {user.goals}\n' \
              f'<b>Город:</b> {user.city}\n' \
              f'<b>Откуда узнал о школе:</b> {user.source_of_knowledge}\n' \
              f'<b>Комментарий тимлида:</b> {user.lead_description}\n' \
              f'<b>Время присоединения:</b> {user.join_time}\n'
    if user.is_approved == 1:
        caption += '\n<b>Анкета проверена</b>\n'
    if user.is_moderator == 1:
        caption += '<b>Модератор</b>\n'
    try:
        await bot.send_photo(chat_id, user.photo, caption=caption,
                             reply_markup=reply_markup)
    except BadRequest:
        await bot.send_message(chat_id, caption + '\n<b>Фото отсутствует в бд</b>',
                               reply_markup=reply_markup)


async def send_full_card(chat_id: int, user: User, reply_markup=ReplyKeyboardRemove()) -> None:
    caption = f'<b>Системная информация</b>\n\n'\
                                                \
              f'<b>ID:</b> {user.user_id}\n' \
              f'<b>TG ID:</b> {user.telegram_id}\n' \
              f'<b>Почта:</b> {user.email}\n' \
              f'<b>Git или Behance:</b> {user.git}{user.behance}\n\n' \
                                                                      \
              f'<b>Общая информация:</b>\n\n' \
                                              \
              f'<b>ФИО:</b> {user.surname} {user.name} {user.patronymic}\n' \
              f'<b>Пол:</b> {user.gender}\n' \
              f'<b>Логин в Telegram:</b> {user.tg_login}\n' \
              f'<b>Желаемый отдел:</b> {user.desired_department}\n' \
              f'<b>Скилы:</b> {user.skills}\n' \
              f'<b>Цели:</b> {user.goals}\n' \
              f'<b>Город:</b> {user.city}\n' \
              f'<b>Откуда узнал о школе:</b> {user.source_of_knowledge}\n' \
              f'<b>Комментарий тимлида:</b> {user.lead_description}\n' \
              f'<b>Время присоединения:</b> {user.join_time}\n'
    if user.is_approved == 1:
        caption += f'\n<b>Анкета проверена</b>\n'
    if user.is_moderator == 1:
        caption += f'<b>Модератор</b>\n'
    try:
        await bot.send_photo(chat_id, user.photo, caption=caption,
                             reply_markup=reply_markup)
    except BadRequest:
        await bot.send_message(chat_id, caption + f'\n<b>Фото отсутствует в бд</b>',
                               reply_markup=reply_markup)