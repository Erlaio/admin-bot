from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class AgreementKeyboard(ButtonFactory):
    AGREE_WITH_RULES = 'Я согласен с правилами 😎'
    DONT_AGREE_WITH_RULES = 'Я не согласен с правилами 🤔'

    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=AGREE_WITH_RULES),
             KeyboardButton(text=DONT_AGREE_WITH_RULES)]
        ],
        resize_keyboard=True,
    )
