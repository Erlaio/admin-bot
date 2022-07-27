from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ProjectCommandsKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(text='Создать новый проект'),
        KeyboardButton(text='Удалить проект'),
        KeyboardButton(text='Сменить имя проекта'),
    ).insert(
        KeyboardButton(text='Сменить/добавить тим лида проекта'))
