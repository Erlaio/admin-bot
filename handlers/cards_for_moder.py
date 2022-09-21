from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default.inline_keyboards import ModeratorInlineKeyboard, BackInlineKeyboard, \
    ModeratorChangeCardInlineKeyboard
from keyboard.default.pagination import Pagination, InlineKeyboardButton
from loader import dp, bot
from pkg.db.user_func import get_user_by_tg_id, get_all_users, update_field_value
from utils.context_helper import ContextHelper
from utils.send_card import send_card


@dp.message_handler(commands='change_card_by_moder')
async def change_card_by_moder(message: types.Message, state: FSMContext):
    # try:
    user = await get_user_by_tg_id(message.from_user.id)
    if user.is_moderator:
        await send_character_page_for_edit(message)
    else:
        await message.answer('Вы не модератор',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


# except (TypeError, AttributeError):
#     await message.answer('Вас нет в базе, пожалуйста пройдите регистрацию',
#                          reply_markup=ReplyKeyboardRemove())
#     await state.finish()


async def send_character_page_for_edit(message: types.Message, page=1):
    user_list = await get_all_users()
    if user_list:
        paginator = Pagination(
            len(user_list),
            current_page=page,
            data_pattern='user_for_change#{page}'
        )
        user = user_list[page - 1]
        list_of_buttons = ModeratorChangeCardInlineKeyboard(page, user).get_inline_keyboard(is_key=True)
        for buttons in list_of_buttons:
            paginator.add_before(
                *buttons)
        paginator.add_after(
            *BackInlineKeyboard().get_inline_keyboard(is_key=True)
        )
        await send_card(
            message.chat.id,
            user=user_list[page - 1],
            reply_markup=paginator.markup,
        )
    else:
        await message.answer('Пользователей нет в базе данных', reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'change')
async def characters_for_edit_page_callback(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split('#')
    print(call_data)
    if len(call_data) == 5:
        _, page, field_name, field_value, telegram_id = call_data
        await bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        await ContextHelper.add_tg_id(telegram_id=telegram_id, context=state)
        await ContextHelper.add_some_data(data=field_name, context=state)
        await bot.send_message(call.message.chat.id, f'Выбрано поле {field_name} со значением {field_value}')
        await state.set_state('change')
    else:
        _, page = call_data
        await bot.delete_message(
            call.message.chat.id,
            call.message.message_id
        )
        await send_character_page_for_edit(call.message, int(page))


@dp.callback_query_handler(lambda call: call.data.split('#')
                           [0] == 'user_for_change')
async def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await send_character_page_for_edit(call.message, page)


@dp.message_handler(state='change')
async def change_data_of_user(message: types.Message, state: FSMContext):
    telegram_id = await ContextHelper.get_tg_id(state)
    field_name = await ContextHelper.get_some_data(state)
    answer = message.text
    await update_field_value(telegram_id=telegram_id, field=field_name, value=answer)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Описание было изменено на {answer}')
    await state.finish()
