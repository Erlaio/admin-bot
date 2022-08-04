from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default.pagination import Pagination, InlineKeyboardButton
from loader import dp
from pkg.db.user_func import get_user_by_tg_id, get_all_users
from utils.send_card import send_card


@dp.message_handler(commands='add_lead_description')
async def add_lead_description(message: types.Message, state: FSMContext):
    try:
        user = await get_user_by_tg_id(message.from_user.id)
        if user.is_moderator:
            await send_character_page(message)
        else:
            await message.answer('Вы не модератор',
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
    except (TypeError, AttributeError):
        await message.answer('Вас нет в базе, пожалуйста пройдите регистрацию',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


async def send_character_page(message: types.Message, page=1):
    user_list = await get_all_users()
    if user_list:
        paginator = Pagination(
            page_count=len(user_list),
            current_page=page,
            data_pattern='user#{page}'
        )

        paginator.add_before(
            InlineKeyboardButton(
                text='Исправить описание тимлида',
                callback_data='change_description#{}'.format(user_list[page - 1])
            )
        )

        paginator.add_after(
            InlineKeyboardButton(
                'Вернуться на главную',
                callback_data='back')
        )

        await send_card(
            message.chat.id,
            user=user_list[page - 1],
            reply_markup=paginator.markup,
        )
    else:
        await message.answer('База пуста', reply_markup=ReplyKeyboardRemove())
