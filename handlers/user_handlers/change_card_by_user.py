from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove, InlineKeyboardMarkup

from keyboard.default.inline_keyboards import UserChangeCardInlineKeyboard, ModeratorChangeDecisionInlineKeyboard
from keyboard.default.keyboards import StopBotKeyboard, DepartmentsKeyboard
from loader import dp, bot
from pkg.db.user_func import get_user_by_tg_id, update_field_value
from pkg.settings import settings
from utils import validations
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
        text = 'Выберите, пожалуйста, В какой бы отдел хотели попасть?'
        reply_markup = await DepartmentsKeyboard.get_reply_keyboard()
    await bot.send_message(call.message.chat.id,
                           text=text,
                           reply_markup=reply_markup)
    await state.set_state('change_by_user')


@dp.message_handler(state='change_by_user')
async def change_data_of_user(message: types.Message, state: FSMContext):
    telegram_id = await ContextHelper.get_tg_id(state)
    user = await get_user_by_tg_id(tg_id=int(telegram_id))
    user_dict = dict(user)
    field_name = await ContextHelper.get_some_data(state)
    answer = message.text
    if not await validations.Validations(field_name, message).validate_tg_login_email_git():
        await state.set_state('change_by_user')
    else:
        await bot.send_message(chat_id=settings.TELEGRAM_MODERS_CHAT_ID,
                               text=f'Поступил запрос от {user.tg_login} на изменение поля {field_name} '
                                    f'со значения {user_dict[field_name]} на значение {answer}')
        await send_full_card(chat_id=settings.TELEGRAM_MODERS_CHAT_ID, user=user,
                             reply_markup=ModeratorChangeDecisionInlineKeyboard(
                                 telegram_id=user.telegram_id,
                                 field_name=field_name,
                                 field_value=answer
                             ).get_inline_keyboard())
        await message.answer('Ваш запрос был направлен модераторам на рассмотрение. '
                             'Как только решение будет принято, Вы будете уведомлены в этом чате',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'approve_changes')
async def edit_approved(call: types.CallbackQuery, state: FSMContext):
    _, telegram_id, field_name, field_value = call.data.split('#')
    moder_tg = call['from']['username']
    user = await get_user_by_tg_id(int(telegram_id))

    await update_field_value(telegram_id=int(telegram_id), field=field_name, value=field_value)
    await bot.send_message(chat_id=settings.TELEGRAM_MODERS_CHAT_ID,
                           text=f'Запрос {user.tg_login} на изменение был одобрен @{moder_tg}\n\n'
                                f'Поле {field_name} изменено на {field_value}')
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=None)
    await bot.send_message(chat_id=user.telegram_id,
                           text=f'Выбранное поле теперь имеет значение: {field_value}',
                           reply_markup=ReplyKeyboardRemove())
    await state.finish()


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'decline_changes')
async def edit_declined(call: types.CallbackQuery, state: FSMContext):
    _, telegram_id, field_name, field_value = call.data.split('#')
    moder_tg = call['from']['username']
    user = await get_user_by_tg_id(int(telegram_id))

    await bot.send_message(chat_id=settings.TELEGRAM_MODERS_CHAT_ID,
                           text=f'Запрос {user.tg_login} на изменение был отклонен @{moder_tg}\n\n'
                                f'Поле {field_name} НЕ изменено на {field_value}')
    await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                        message_id=call.message.message_id,
                                        reply_markup=None)
    await bot.send_message(chat_id=user.telegram_id,
                           text=f'К сожалению, модераторы отклонили Вашу заявку на изменение данных.',
                           reply_markup=ReplyKeyboardRemove())
    await state.finish()
