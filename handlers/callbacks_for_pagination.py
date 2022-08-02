from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.moders_output import characters_page_callback
from loader import dp, bot
from pkg.db.user_func import update_user_approve, delete_user_by_tg_id, get_random_moder
from utils.send_card import send_card


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'approve')
async def callback_approve(call):
    _, page, telegram_id = call.data.split('#')
    await update_user_approve(telegram_id)
    await bot.send_message(call.message.chat.id, f'Пользователь добавлен')
    if page == '0':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        await characters_page_callback(call)


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'refilling')
async def callback_refilling(call):
    _, page, telegram_id = call.data.split('#')
    await bot.send_message(chat_id=telegram_id,
                           text='Неверно заполнена анкета, заполните как в примере')
    user = await get_random_moder()
    await send_card(telegram_id, user)
    await bot.send_message(call.message.chat.id, f'Пользователь отправлен на перезаполнение')
    if page == '0':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        await characters_page_callback(call)


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'delete_user')
async def callback_delete_user(call):
    _, page, telegram_id = call.data.split('#')
    await delete_user_by_tg_id(telegram_id=telegram_id)
    await bot.send_message(call.message.chat.id, 'Пользователь удален')
    if page == '0':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        await characters_page_callback(call)


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'back')
async def callback_back(call, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Возвращаю на главную',
                           reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await state.finish()
