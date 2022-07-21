from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default import Keyboard
from loader import dp
from pkg.db.department_func import *
from pkg.db.user_func import get_user_by_tg_id
from states.department_utils_state import DepartmentUtilsState
from utils.check_department_is_available import is_department_available


@dp.message_handler(commands='department_utils')
async def start_handler(message: types.Message, state: FSMContext):
    try:
        user = get_user_by_tg_id(message.from_user.id)
        if user.is_moderator:
            await message.answer('Что вы хотите сделать?',
                                 reply_markup=Keyboard.DEPARTMENTS_UTILS)
            await DepartmentUtilsState.moderator_choice.set()
        else:
            await message.answer('Вы не модератор',
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
    except TypeError:
        await message.answer('Вас нет в базе, пожалуйста пройдите регистрацию')
        await state.finish()


@dp.message_handler(state=DepartmentUtilsState.moderator_choice)
async def moderator_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Создать новый отдел':
        await message.answer('Введите название отдела который хотите создать',
                             reply_markup=ReplyKeyboardRemove())
        await DepartmentUtilsState.new_department.set()
    elif answer == 'Удалить отдел':
        await message.answer('Введите название отдела который хотите удалить',
                             reply_markup=ReplyKeyboardRemove())
        await DepartmentUtilsState.delete_department.set()
    elif answer == 'Сменить имя отдела':
        await message.answer('Введите название отдела который хотите поменять',
                             reply_markup=ReplyKeyboardRemove())
        await DepartmentUtilsState.change_department_name_get_name.set()
    elif answer == 'Сменить/добавить тим лида отдела':
        await message.answer('Введите название отдела тим лидера которого вы хотите поменять',
                             reply_markup=ReplyKeyboardRemove())
        await DepartmentUtilsState.change_team_lead_name_get_name.set()
    else:
        await message.answer(f'⚠️ {answer} неверный ответ.',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(state=DepartmentUtilsState.new_department)
async def new_department(message: types.Message, state: FSMContext):
    department_name = message.text
    add_new_department(department_name)
    await message.answer(f'Отдел {department_name} создан')
    await state.finish()


@dp.message_handler(state=DepartmentUtilsState.delete_department)
async def delete_department(message: types.Message, state: FSMContext):
    department_name = message.text
    if is_department_available(message):
        delete_department_by_name(department_name)
        await message.answer(f'Отдел {department_name} удален')
        await state.finish()
    else:
        await message.answer('Такого отдела нет')
        await state.finish()


@dp.message_handler(state=DepartmentUtilsState.change_department_name_get_name)
async def get_new_department_name(message: types.Message, state: FSMContext):
    if is_department_available(message):
        await message.answer('Введите новое название отдела')
        await state.update_data(old_name=message.text)
        await DepartmentUtilsState.change_department_name.set()
    else:
        await message.answer('Такого отдела нет')
        await state.finish()


@dp.message_handler(state=DepartmentUtilsState.change_department_name)
async def change_department_name(message: types.Message, state: FSMContext):
    new_name = message.text
    old_name_dict = await state.get_data()
    old_name = old_name_dict.get('old_name', '')
    update_department_name(old_name, new_name)
    await message.answer(f'Отдел {old_name} переименован в {new_name}')
    await state.finish()


@dp.message_handler(state=DepartmentUtilsState.change_team_lead_name_get_name)
async def get_new_team_lead_name(message: types.Message, state: FSMContext):
    if is_department_available(message):
        await message.answer('Введите новое имя Тим лида отдела')
        await state.update_data(department=message.text)
        await DepartmentUtilsState.change_team_lead_name.set()
    else:
        await message.answer('Такого отдела нет')
        await state.finish()


@dp.message_handler(state=DepartmentUtilsState.change_team_lead_name)
async def change_team_lead_name(message: types.Message, state: FSMContext):
    new_tl_name = message.text
    department_name_dict = await state.get_data()
    department_name = department_name_dict.get('department', '')
    try:
        attach_tl_to_department(department_name, new_tl_name)
    except TypeError:
        await message.answer('Неверное название отдела')
    else:
        await message.answer(f'К отделу {department_name} прикреплен Тим лид: {new_tl_name}')
    finally:
        await state.finish()
