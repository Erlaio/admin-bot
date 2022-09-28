from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default.keyboards import ProjectCommandsKeyboard, StopBotKeyboard
from loader import dp
from pkg.db.project_func import *
from pkg.db.user_func import get_user_by_tg_id
from states.project_states import ProjectStates
from utils.check_is_available import is_project_available


@dp.message_handler(commands='project')
async def start_handler(message: types.Message, state: FSMContext):
    try:
        user = await get_user_by_tg_id(message.from_user.id)
        if user.is_moderator:
            await message.answer('Что вы хотите сделать?',
                                 reply_markup=ProjectCommandsKeyboard.get_reply_keyboard())
            await ProjectStates.moderator_choice.set()
        else:
            await message.answer('Вы не модератор',
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
    except (TypeError, AttributeError):
        await message.answer('Вас нет в базе, пожалуйста пройдите регистрацию')
        await state.finish()


@dp.message_handler(state=ProjectStates.moderator_choice)
async def moderator_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == ProjectCommandsKeyboard.A_CREATE_PROJECT:
        await message.answer('Введите название проекта который хотите создать',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await ProjectStates.new_project.set()
    elif answer == ProjectCommandsKeyboard.B_DELETE_PROJECT:
        await message.answer('Введите название проекта который хотите удалить',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await ProjectStates.delete_project.set()
    elif answer == ProjectCommandsKeyboard.C_CHANGE_PROJECT_NAME:
        await message.answer('Введите название проекта который хотите поменять',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await ProjectStates.change_project_name_get_name.set()
    elif answer == ProjectCommandsKeyboard.D_CHANGE_PROJECT_LEAD:
        await message.answer('Введите название проекта тим лидера которого вы хотите поменять',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await ProjectStates.change_team_lead_name_get_name.set()
    else:
        await message.answer(f'⚠️ {answer} неверный ответ.',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(state=ProjectStates.new_project)
async def new_department(message: types.Message, state: FSMContext):
    project_name = message.text
    await add_new_project(project_name)
    await message.answer(f'Проект "{project_name}" создан')
    await state.finish()


@dp.message_handler(state=ProjectStates.delete_project)
async def delete_department(message: types.Message, state: FSMContext):
    if await is_project_available(message.text):
        await delete_project_by_name(message.text)
        await message.answer(f'Проект "{message.text}" удален')
        await state.finish()
    else:
        await message.answer('Такого проекта нет')
        await state.finish()


@dp.message_handler(state=ProjectStates.change_project_name_get_name)
async def get_new_department_name(message: types.Message, state: FSMContext):
    if await is_project_available(message.text):
        await message.answer('Введите новое название проекта', reply_markup=StopBotKeyboard.get_reply_keyboard())
        await state.update_data(old_name=message.text)
        await ProjectStates.change_project_name.set()
    else:
        await message.answer('Такого проекта нет')
        await state.finish()


@dp.message_handler(state=ProjectStates.change_project_name)
async def change_department_name(message: types.Message, state: FSMContext):
    old_name_dict = await state.get_data()
    old_name = old_name_dict.get('old_name', '')
    await update_project_name(old_name, message.text)
    await message.answer(f'Проект "{old_name}" переименован в "{message.text}"')
    await state.finish()


@dp.message_handler(state=ProjectStates.change_team_lead_name_get_name)
async def get_new_team_lead_name(message: types.Message, state: FSMContext):
    if await is_project_available(message.text):
        await message.answer('Введите новое имя Тим лида проекта', reply_markup=StopBotKeyboard.get_reply_keyboard())
        await state.update_data(department=message.text)
        await ProjectStates.change_team_lead_name.set()
    else:
        await message.answer('Такого проекта нет')
        await state.finish()


@dp.message_handler(state=ProjectStates.change_team_lead_name)
async def change_team_lead_name(message: types.Message, state: FSMContext):
    project_name_dict = await state.get_data()
    project_name = project_name_dict.get('department', '')
    await attach_tl_to_project(project_name, message.text)
    await message.answer(f'К проекту "{project_name}" прикреплен Тим лид: "{message.text}"')
    await state.finish()
