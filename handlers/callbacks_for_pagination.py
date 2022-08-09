from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.moders_output import characters_page_callback
from loader import dp, bot
from pkg.db.user_func import delete_user_by_tg_id, update_user_approve


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'approve')
async def callback_approve(call):
    _, page, telegram_id, user_name = call.data.split('#')
    await update_user_approve(telegram_id)
    await bot.send_message(call.message.chat.id, f'Пользователь {user_name} добавлен')
    await bot.send_message(telegram_id, text='Анкета обновлена, проверьте состояние')
    if page == '0':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        await characters_page_callback(call)


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'refilling')
async def callback_refilling(call):
    _, page, telegram_id, user_name = call.data.split('#')
    await delete_user_by_tg_id(telegram_id)
    await bot.send_message(call.message.chat.id, f'Пользователь {user_name} отправлен на перезаполнение')
    await bot.send_message(telegram_id, text='Анкета обновлена, проверьте состояние')
    if page == '0':
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    else:
        await characters_page_callback(call)


@dp.callback_query_handler(lambda call: call.data.split('#')
                                        [0] == 'delete_user')
async def callback_delete_user(call):
    _, page, telegram_id, user_name = call.data.split('#')
    await delete_user_by_tg_id(telegram_id)
    await bot.send_message(call.message.chat.id, f'Пользователь {user_name} удален')
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