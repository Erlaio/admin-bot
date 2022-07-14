from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboard.default.constant_buttons_value import READ_RULES, DONT_READ_RULES, AGREE_WITH_RULES, \
    DONT_AGREE_WITH_RULES, MALE_GENDER, FEMALE_GENDER, WANT_UPLOAD_PHOTO, DONT_WANT_UPLOAD_PHOTO, YES, NO, CHECK_ACCESS

choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=READ_RULES),
            KeyboardButton(text=DONT_READ_RULES)
        ]
    ],
    resize_keyboard=True
)

agreement = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=AGREE_WITH_RULES),
            KeyboardButton(text=DONT_AGREE_WITH_RULES)
        ]
    ],
    resize_keyboard=True
)

gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=MALE_GENDER),
            KeyboardButton(text=FEMALE_GENDER)
        ]
    ],
    resize_keyboard=True
)

photo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=WANT_UPLOAD_PHOTO),
            KeyboardButton(text=DONT_WANT_UPLOAD_PHOTO)
        ]
    ],
    resize_keyboard=True
)

universal_choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=YES),
            KeyboardButton(text=NO)
        ]
    ],
    resize_keyboard=True
)

check_access = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=CHECK_ACCESS),
        ]
    ],
    resize_keyboard=True
)



