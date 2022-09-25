from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram import types


@dp.message_handler(CommandHelp())
async def start_handler(message: types.Message, state: FSMContext):
    command_bot = '<b>Общие команды:</b>\n\n' \
                  '/start - начать работу с ботом.\n\n' \
                  '/help - помощь по командам взаимодействия с ботом.\n\n' \
                  '/show_card - посмотреть личные карточки студентов Школы IT.\n\n' \
                  '/show_department_cards - показать карточки пользователей отдела.\n\n' \
                  '/moder - меню модератора.\n\n' \
                  '/rules - правила Школы IT.\n\n\n'
    await message.answer(command_bot)
    await state.finish()
