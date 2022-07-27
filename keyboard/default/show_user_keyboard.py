from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ShowUserKeyboard(ButtonFactory):
    VIEW_ALL = 'Посмотреть всех'
    VIEW_ID = 'Посмотреть по ID'
    VIEW_TG_LOGIN = 'Посмотреть по Логину в Telegram'

    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=VIEW_ALL),
                KeyboardButton(text=VIEW_ID),
                KeyboardButton(text=VIEW_TG_LOGIN)
            ]
        ],
        resize_keyboard=True
    )
