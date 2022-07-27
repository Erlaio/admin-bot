from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class CheckAccessKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text='Проверить состояние анкеты ✅'),
            ]
        ],
        resize_keyboard=True
    )
