from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram import types


@dp.message_handler(CommandHelp())
async def start_handler(message: types.Message, state: FSMContext):
    command_bot = '/start - начать работу с ботом.\n' \
                  '/department - добавить новый отдел или изменить данные о существующем.\n' \
                  '/project -  добавить новый проект или изменить данные о существующем.\n' \
                  '/show_card - посмотреть личные карточки студентов Школы IT.\n' \
                  '/show_department_cards - вывести список всех участников отдела.\n'
    await message.answer(command_bot)
    await state.finish()
