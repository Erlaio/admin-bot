from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp, bot
from pkg.db.user_func import update_user_approve, delete_user_by_id


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'approve')
async def callback_approve(call):
    await update_user_approve(user_id=call.data.split('#')[2])
    await bot.send_message(call.message.chat.id, 'Пользователь добавлен')


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'refilling')
async def callback_refilling(call):
    pass
    # TODO


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'delete_user')
async def callback_delete_user(call):
    await delete_user_by_id(user_id=call.data.split('#')[2])
    await bot.send_message(call.message.chat.id, 'Пользователь удален')


@dp.callback_query_handler(lambda call: call.data.split('#')[0] == 'back')
async def callback_back(call, state: FSMContext):
    await bot.send_message(call.message.chat.id, 'Возвращаю на главную',
                           reply_markup=ReplyKeyboardRemove())
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await state.finish()
