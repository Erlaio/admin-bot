from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ShowUserKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Посмотреть всех'),
                KeyboardButton(text='Посмотреть по ID'),
                KeyboardButton(text='Посмотреть по Логину в Telegram')
            ]
        ],
        resize_keyboard=True
    )
