from aiogram import types

from keyboard.default.pagination import *

from loader import dp, bot
from pkg.db.user_func import get_unapproved_users
from utils.send_card import send_card


@dp.message_handler(commands='review_cards')
async def start_review(message: types.Message):
    await send_character_page(message)


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'character')
async def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await send_character_page(call.message, page)


async def send_character_page(message: types.Message, page=1):
    user_list = get_unapproved_users()
    paginator = Pagination(
        len(user_list),
        current_page=page,
        data_pattern='character#{page}'
    )

    paginator.add_before(
        InlineKeyboardButton('Одобрить', callback_data='approve#{}'.format(page)),
        InlineKeyboardButton('Перезаполнение', callback_data='refilling#{}'.format(page)),
        InlineKeyboardButton('Удалить', callback_data='delete_user#{}'.format(page))
    )
    paginator.add_after(InlineKeyboardButton('Go back', callback_data='back'))

    await send_card(
        message,
        user=user_list[page - 1],
        reply_markup=paginator.markup,
        )
