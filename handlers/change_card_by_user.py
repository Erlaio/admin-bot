import validators
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup

from keyboard.default.inline_keyboards import BackInlineKeyboard, ModeratorChangeCardInlineKeyboard, \
    UserChangeCardInlineKeyboard
from keyboard.default.keyboards import StopBotKeyboard, DepartmentsKeyboard
from keyboard.default.pagination import Pagination
from loader import dp, bot
from pkg.db.user_func import get_user_by_tg_id, get_all_users, update_field_value
from utils.context_helper import ContextHelper
from utils.send_card import send_card, send_full_card


@dp.message_handler(commands='change_card')
async def change_card_by_moder(message: types.Message, state: FSMContext):
    try:
        await get_user_by_tg_id(message.from_user.id)
        await send_character_page_for_edit(message)
    except (TypeError, AttributeError):
        await message.answer('Вас нет в базе, пожалуйста пройдите регистрацию',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


async def send_character_page_for_edit(message: types.Message):
    user = await get_user_by_tg_id(message.from_user.id)
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=UserChangeCardInlineKeyboard(page=1,
                                                     user=user,
                                                     callback_data='change_by_user',
                                                     back_button=True).
        get_inline_keyboard(is_key=True))
    await send_card(chat_id=message.chat.id,
                    user=user,
                    reply_markup=reply_markup)


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'change_by_user')
async def characters_for_edit_page_callback(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split('#')
    _, page, field_name, telegram_id = call_data
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await ContextHelper.add_tg_id(telegram_id=telegram_id, context=state)
    await ContextHelper.add_some_data(data=field_name, context=state)
    reply_markup = StopBotKeyboard.get_reply_keyboard()
    text = 'Введите, пожалуйста, на какое значение хотите изменить выбранные данные'
    if field_name == 'desired_department':
        text = f'Выберите, пожалуйста, В какой бы отдел хотели попасть?'
        reply_markup = await DepartmentsKeyboard.get_reply_keyboard()
    await bot.send_message(call.message.chat.id,
                           text=text,
                           reply_markup=reply_markup)
    await state.set_state('change_by_user')


# @dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'user_for_change')
# async def characters_page_callback(call):
#     await bot.delete_message(
#         call.message.chat.id,
#         call.message.message_id
#     )
#     await send_character_page_for_edit(call.message)


@dp.message_handler(state='change_by_user')
async def change_data_of_user(message: types.Message, state: FSMContext):
    telegram_id = await ContextHelper.get_tg_id(state)
    field_name = await ContextHelper.get_some_data(state)
    answer = message.text

    if field_name == 'tg_login' and not answer.startswith('@'):
        await message.answer('Пожалуйста, введите ваш логин с @\n(Например: @login)',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    elif field_name == 'email' and not validators.email(answer):
        await message.answer('Вы ввели неверный формат почты',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    elif field_name == 'git' or field_name == 'behance' and not validators.url(answer):
        await message.answer('Введите, пожалуйста, корректную ссылку',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())

    await update_field_value(telegram_id=telegram_id, field=field_name, value=answer)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Выбранное поле теперь имеет значение: {answer}',
                           reply_markup=ReplyKeyboardRemove())
    await state.finish()
