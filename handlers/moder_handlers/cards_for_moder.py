from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default.inline_keyboards import BackInlineKeyboard, ModeratorChangeCardInlineKeyboard
from keyboard.default.keyboards import StopBotKeyboard
from keyboard.default.pagination import Pagination, InlineKeyboardButton
from loader import dp, bot
from pkg.db.user_func import get_user_by_tg_id, get_all_users, update_field_value, delete_user_by_tg_id
from pkg.settings import settings
from utils import validations
from utils.context_helper import ContextHelper
from utils.delete_user import delete_user
from utils.send_card import send_full_card


@dp.message_handler(commands='change_card_by_moder')
async def change_card_by_moder(message: types.Message, state: FSMContext):
    try:
        user = await get_user_by_tg_id(message.from_user.id)
        if user.is_moderator:
            await send_character_page_for_edit(message)
        else:
            await message.answer('Вы не модератор',
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
    except (TypeError, AttributeError):
        await message.answer('Вас нет в базе, пожалуйста пройдите регистрацию',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


async def send_character_page_for_edit(message: types.Message, page=1):
    user_list = await get_all_users()
    if user_list:
        paginator = Pagination(
            len(user_list),
            current_page=page,
            data_pattern='user_for_change#{page}'
        )
        user = user_list[page - 1]
        list_of_buttons = ModeratorChangeCardInlineKeyboard(page, user, 'change_by_moder').\
            get_inline_keyboard(is_key=True)
        for buttons in list_of_buttons:
            paginator.add_before(
                *buttons)
        paginator.add_after(
            InlineKeyboardButton(text='Удалить',
                                 callback_data=f'delete_user_by_menu#{page}#{user.telegram_id}#{user.tg_login}')
        )
        paginator.add_after(
            *BackInlineKeyboard().get_inline_keyboard(is_key=True)
        )
        await send_full_card(
            message.chat.id,
            user=user_list[page - 1],
            reply_markup=paginator.markup,
        )
    else:
        await message.answer('Пользователей нет в базе данных', reply_markup=ReplyKeyboardRemove())


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'change_by_moder')
async def characters_for_edit_page_callback(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data.split('#')
    _, page, field_name, telegram_id = call_data
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await ContextHelper.add_tg_id(telegram_id=telegram_id, context=state)
    await ContextHelper.add_some_data(data=field_name, context=state)
    await bot.send_message(call.message.chat.id,
                           f'Выбрано поле {field_name}. Введите, пожалуйста,'
                           f' значение, на которое хотите изменить данные',
                           reply_markup=StopBotKeyboard.get_reply_keyboard())
    await state.set_state('change_by_moder')


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'user_for_change')
async def characters_page_callback(call):
    page = int(call.data.split('#')[1])
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await send_character_page_for_edit(call.message, page)


@dp.message_handler(state='change_by_moder')
async def change_data_of_user(message: types.Message, state: FSMContext):
    telegram_id = await ContextHelper.get_tg_id(state)
    field_name = await ContextHelper.get_some_data(state)
    answer = message.text
    if not await validations.Validations(field_name, message).validate_tg_login_email_git():
        await state.set_state('change_by_moder')
    else:
        await update_field_value(telegram_id=telegram_id, field=field_name, value=answer)
        await bot.send_message(chat_id=message.chat.id,
                               text=f'Поле {field_name} теперь имеет значение: {answer}')
        await state.finish()


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'delete_user_by_menu')
async def callback_delete_user(call):
    channels = settings.TELEGRAM_SCHOOL_CHATS
    moder_tg = call['from']['username']
    _, page, telegram_id, user_name = call.data.split('#')

    await delete_user_by_tg_id(telegram_id)
    await bot.send_message(chat_id=settings.TELEGRAM_MODERS_CHAT_ID,
                           text=f'Пользователь {user_name} удален модератором @{moder_tg} вручную')
    await delete_user(telegram_id, channels)
    await bot.send_message(telegram_id, text='Ваша карточка была удалена. Свяжитесь с администратором')
    if page == '0':
        await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                            message_id=call.message.message_id,
                                            reply_markup=None)
    else:
        await send_character_page_for_edit(call.message)
