from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class DepartmentCommandsKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).row(
        KeyboardButton(text='Создать новый отдел'),
        KeyboardButton(text='Удалить отдел'),
        KeyboardButton(text='Сменить имя отдела')).insert(
        KeyboardButton(text='Сменить/добавить тим лида отдела'))
