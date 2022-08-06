from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dp, bot
from pkg.db.user_func import update_lead_description
from utils.context_helper import ContextHelper


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'change_description')
async def callback_change_description(call: types.CallbackQuery, state: FSMContext):
    _, page, telegram_id, user_name = call.data.split('#')
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await ContextHelper.add_tg_id(telegram_id=telegram_id, context=state)
    await bot.send_message(call.message.chat.id, f'Введите описание')
    await state.set_state('change_description')


@dp.message_handler(state='change_description')
async def change_description(message: types.Message, state: FSMContext):
    telegram_id = await ContextHelper.get_tg_id(state)
    answer = message.text
    await update_lead_description(telegram_id=telegram_id, description=answer)
    await bot.send_message(chat_id=message.chat.id,
                           text=f'Описание было изменено на {answer}')
    await state.finish()
