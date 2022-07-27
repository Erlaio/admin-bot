from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default import Keyboard
from keyboard.default.keyboard import DepartmentButtonFactory
from loader import dp
from pkg.db.department_func import *
from pkg.db.user_func import get_user_by_tg_id, update_user_department
from states.department_states import DepartmentStates
from utils.check_is_available import is_department_available


@dp.message_handler(commands='department')
async def start_handler(message: types.Message, state: FSMContext):
    try:
        user = await get_user_by_tg_id(message.from_user.id)
        if user.is_moderator:
            await message.answer('Что вы хотите сделать?',
                                 reply_markup=Keyboard.DEPARTMENTS_COMMANDS)
            await DepartmentStates.moderator_choice.set()
        else:
            await message.answer('Вы не модератор',
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
    except (TypeError, AttributeError):
        await message.answer('Вас нет в базе, пожалуйста пройдите регистрацию')
        await state.finish()


@dp.message_handler(state=DepartmentStates.moderator_choice)
async def moderator_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Создать новый отдел':
        await message.answer('Введите название отдела который хотите создать',
                             reply_markup=ReplyKeyboardRemove())
        await DepartmentStates.new_department.set()
    elif answer == 'Удалить отдел':
        await message.answer('Введите название отдела который хотите удалить',
                             reply_markup=ReplyKeyboardRemove())
        await DepartmentStates.delete_department.set()
    elif answer == 'Сменить имя отдела':
        await message.answer('Введите название отдела который хотите поменять',
                             reply_markup=ReplyKeyboardRemove())
        await DepartmentStates.change_department_name_get_name.set()
    elif answer == 'Сменить/добавить тим лида отдела':
        await message.answer('Введите название отдела тим лидера которого вы хотите поменять',
                             reply_markup=ReplyKeyboardRemove())
        await DepartmentStates.change_team_lead_name_get_name.set()
    else:
        await message.answer(f'⚠️ {answer} неверный ответ.',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(state=DepartmentStates.new_department)
async def new_department(message: types.Message, state: FSMContext):
    department_name = message.text
    if await DepartmentButtonFactory.is_exist(department_name) is False:
        await add_new_department(department_name)
        await DepartmentButtonFactory.add(department_name)
        await message.answer(f'Отдел {department_name} создан')
        await state.finish()
    else:
        await message.answer(f'Отдел {department_name} уже существует')
        await state.finish()


@dp.message_handler(state=DepartmentStates.delete_department)
async def delete_department(message: types.Message, state: FSMContext):
    department_name = message.text
    if await is_department_available(department_name) and await DepartmentButtonFactory.is_exist(department_name):
        await update_user_department(message.text, 'EmptyDepartment')
        await delete_department_by_name(message.text)
        await DepartmentButtonFactory.delete(department_name)
        await message.answer(f'Отдел {message.text} удален')
        await state.finish()
    else:
        await message.answer('Такого отдела нет')
        await state.finish()


@dp.message_handler(state=DepartmentStates.change_department_name_get_name)
async def get_new_department_name(message: types.Message, state: FSMContext):
    if await is_department_available(message.text):
        await message.answer('Введите новое название отдела')
        await state.update_data(old_name=message.text)
        await DepartmentStates.change_department_name.set()
    else:
        await message.answer('Такого отдела нет')
        await state.finish()


@dp.message_handler(state=DepartmentStates.change_department_name)
async def change_department_name(message: types.Message, state: FSMContext):
    old_name_dict = await state.get_data()
    old_name = old_name_dict.get('old_name', '')
    if await DepartmentButtonFactory.is_exist(old_name):
        new_name = message.text
        await update_department_name(old_name, new_name)
        await DepartmentButtonFactory.rename(old_name=old_name, new_name=new_name)
        await message.answer(f'Отдел {old_name} переименован в {new_name}')
        await state.finish()
    else:
        await message.answer(f'{old_name} не существует')
        await state.finish()


@dp.message_handler(state=DepartmentStates.change_team_lead_name_get_name)
async def get_new_team_lead_name(message: types.Message, state: FSMContext):
    if await is_department_available(message.text):
        await message.answer('Введите новое имя Тим лида отдела')
        await state.update_data(department=message.text)
        await DepartmentStates.change_team_lead_name.set()
    else:
        await message.answer('Такого отдела нет')
        await state.finish()


@dp.message_handler(state=DepartmentStates.change_team_lead_name)
async def change_team_lead_name(message: types.Message, state: FSMContext):
    department_name_dict = await state.get_data()
    department_name = department_name_dict.get('department', '')
    await attach_tl_to_department(department_name, message.text)
    await message.answer(f'К отделу {department_name} прикреплен Тим лид: {message.text}')
    await state.finish()
