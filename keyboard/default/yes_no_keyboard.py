from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class YesNoKeyboard(ButtonFactory):
    YES = 'Да ✅'
    NO = 'Нет ❌'

    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=YES),
                KeyboardButton(text=NO)
            ]
        ],
        resize_keyboard=True
    )
