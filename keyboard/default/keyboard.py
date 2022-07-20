from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from keyboard.default.button_value import ButtonValue as button


class Keyboard:
    CHOICE = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.READ_RULES),
                KeyboardButton(text=button.DONT_READ_RULES)
            ]
        ],
        resize_keyboard=True
    )

    AGREEMENT = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.AGREE_WITH_RULES),
                KeyboardButton(text=button.DONT_AGREE_WITH_RULES)
            ]
        ],
        resize_keyboard=True
    )

    GENDER = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.MALE_GENDER),
                KeyboardButton(text=button.FEMALE_GENDER)
            ]
        ],
        resize_keyboard=True
    )

    PHOTO = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.WANT_UPLOAD_PHOTO),
                KeyboardButton(text=button.DONT_WANT_UPLOAD_PHOTO)
            ]
        ],
        resize_keyboard=True
    )

    UNIVERSAL_CHOICE = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.YES),
                KeyboardButton(text=button.NO)
            ]
        ],
        resize_keyboard=True
    )

    CHECK_ACCESS = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.CHECK_ACCESS),
            ]
        ],
        resize_keyboard=True
    )

    DEPARTMENTS = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.FRONTEND),
                KeyboardButton(text=button.BACKEND),
                KeyboardButton(text=button.ML),
                KeyboardButton(text=button.DS),
                KeyboardButton(text=button.DESIGN),
                KeyboardButton(text=button.MOBILE_DEVELOPMENT),
            ]
        ]
    )
    
    SHOW_USER = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.VIEW_ALL),
                KeyboardButton(text=button.VIEW_SOMEONE)
            ]
        ],
        resize_keyboard=True
    )
