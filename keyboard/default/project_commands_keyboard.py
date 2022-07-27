from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ProjectCommandsKeyboard(ButtonFactory):
    CREATE_PROJECT = 'Создать новый проект'
    DELETE_PROJECT = 'Удалить проект'
    CHANGE_PROJECT_NAME = 'Сменить имя проекта'
    CHANGE_PROJECT_LEAD = 'Сменить/добавить тим лида проекта'

    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(text=CREATE_PROJECT),
        KeyboardButton(text=DELETE_PROJECT),
        KeyboardButton(text=CHANGE_PROJECT_NAME),
    ).insert(
        KeyboardButton(text=CHANGE_PROJECT_LEAD))
