from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class CheckAccessKeyboard(ButtonFactory):
    CHECK_ACCESS = 'Проверить состояние анкеты ✅'

    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=CHECK_ACCESS),
            ]
        ],
        resize_keyboard=True
    )
