from aiogram.dispatcher import FSMContext

from loader import dp
from aiogram.dispatcher.filters.builtin import CommandHelp
from aiogram import types


@dp.message_handler(CommandHelp())
async def start_handler(message: types.Message, state: FSMContext):
    command_bot = '<b>Общие команды:</b>\n\n' \
                  '/start - начать работу с ботом.\n\n' \
                  '/help - Помощь по командам взаимодействия с ботом.\n\n' \
                  '/rules - Правила Школы IT.\n\n\n' \
                  '<b>Команды модераторов:</b>\n\n' \
                  '/department - добавить новый отдел или изменить данные о существующем.\n\n' \
                  '/project -  добавить новый проект или изменить данные о существующем.\n\n' \
                  '/show_card - посмотреть личные карточки студентов Школы IT.\n\n' \
                  '/show_department_cards - вывести список всех участников отдела.\n\n' \
                  '/review_cards - работа со всеми неапрувнутыми учениками'
    await message.answer(command_bot)
    await state.finish()
