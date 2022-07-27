from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class GenderKeyboard(ButtonFactory):
    MALE_GENDER = 'Мужской 👨'
    FEMALE_GENDER = 'Женский 👩‍🦰'

    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=MALE_GENDER),
             KeyboardButton(text=FEMALE_GENDER)]
        ],
        resize_keyboard=True,
    )