from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ChoiceKeyboard(ButtonFactory):
    READ_RULES = 'Ознакомиться с правилами 🤓'
    DONT_READ_RULES = 'Я не буду читать правила 😐'

    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=READ_RULES),
             KeyboardButton(text=DONT_READ_RULES)]
        ],
        resize_keyboard=True,
    )