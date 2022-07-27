from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ProjectCommandsKeyboard(ButtonFactory):
    CREATE_DEPARTMENT = 'Создать новый отдел'
    DELETE_DEPARTMENT = 'Удалить отдел'
    CHANGE_DEPARTMENT_NAME = 'Сменить имя отдела'
    CHANGE_DEPARTMENT_LEAD = 'Сменить/добавить тим лида отдела'

    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(text=CREATE_DEPARTMENT),
        KeyboardButton(text=DELETE_DEPARTMENT),
        KeyboardButton(text=CHANGE_DEPARTMENT_NAME),
    ).insert(
        KeyboardButton(text=CHANGE_DEPARTMENT_LEAD))
