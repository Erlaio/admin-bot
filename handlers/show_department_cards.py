from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from handlers.start import is_command
from keyboard.default.keyboards import DepartmentsKeyboard
from keyboard.default.pagination import Pagination, InlineKeyboardButton
from loader import dp, bot
from pkg.db.user_func import get_users_from_department_name
from states.show_user_state import UserCardState
from utils.check_is_available import is_department_available
from utils.send_card import send_card


@dp.message_handler(commands='show_department_cards')
async def show_user_by_department_start(message: types.Message):
    text = 'Выберите отдел для вывода'
    await message.answer(text,
                         reply_markup=await DepartmentsKeyboard.get_reply_keyboard(one_time=True))
    await UserCardState.show_departments.set()


@dp.callback_query_handler(lambda call: True)
async def characters_page_callback(call, state: FSMContext):
    page = int(call.data.split('#')[1])
    department_name = call.data.split('#')[0]
    await bot.delete_message(
        call.message.chat.id,
        call.message.message_id
    )
    await show_all(department_name, call.message, state=state, page=page)


@dp.message_handler(state=UserCardState.show_departments)
async def show_users_by_department(message: types.Message, state: FSMContext, page=1):
    department_name = message.text
    if not await is_command(department_name):
        if await is_department_available(department_name):
            await message.answer(text=f'Был выбран отдел {department_name}', reply_markup=ReplyKeyboardRemove())
            await show_all(department_name, message, state=state, page=page)
        else:
            await bot.send_message(message.chat.id, 'Такой отдел не найден.',
                                   reply_markup=ReplyKeyboardRemove())
            await state.finish()
    else:
        await message.answer('Вы ввели команду. Выберите, пожалуйста, отдел из клавиатуры'
                             ' или вернитесь на главную страницу')


@dp.message_handler(state=UserCardState.show_all) # вроде как лишний стейт
async def show_all(department_name, message: types.Message, state: FSMContext, page=1):
    user_list = await get_users_from_department_name(department_name=department_name)
    if user_list:
        paginator = Pagination(
            len(user_list),
            current_page=page,
            data_pattern=f'{department_name}#{{page}}'
        )
        paginator.add_after(
            InlineKeyboardButton(
                'Вернуться на главную',
                callback_data='back'))
        await send_card(
            message.chat.id,
            user=user_list[page - 1],
            reply_markup=paginator.markup,
        )
    else:
        await message.answer('Никто не привязан к отделу',
                             reply_markup=ReplyKeyboardRemove())
    await state.finish()
