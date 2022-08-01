from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.callbacks_for_pagination import callback_approve, callback_refilling, callback_delete_user, callback_back
from keyboard.default.pagination import *
from loader import dp, bot
from pkg.db.user_func import get_unapproved_users, update_user_approve, delete_user_by_id
from utils.send_card import send_card


@dp.message_handler(commands='review_cards')
async def start_review(message: types.Message):
    await send_character_page(message)


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'unapproved_character')
async def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await send_character_page(call.message, page)


async def send_character_page(message: types.Message, page=1):
    user_list = await get_unapproved_users()
    if user_list:
        paginator = Pagination(
            len(user_list),
            current_page=page,
            data_pattern='unapproved_character#{page}'
        )

        paginator.add_before(
            InlineKeyboardButton('Одобрить',
                                 callback_data='approve#{}#{}'.format(page, user_list[page - 1].user_id)),
            InlineKeyboardButton('Перезаполнение',
                                 callback_data='refilling#{}#{}'.format(page, user_list[page - 1].user_id)),
            InlineKeyboardButton('Удалить',
                                 callback_data='delete_user#{}#{}'.format(page, user_list[page - 1].user_id)),
        )
        paginator.add_after(InlineKeyboardButton('Вернуться на главную', callback_data='back'))
        await send_card(
            message.chat.id,
            user=user_list[page - 1],
            reply_markup=paginator.markup,
        )
    else:
        await message.answer('Некого апрувить', reply_markup=ReplyKeyboardRemove())
