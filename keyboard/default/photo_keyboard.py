from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class PhotoKeyboard(ButtonFactory):
    WANT_UPLOAD_PHOTO = 'Да! Хочу загрузить свою фоточку 😎'
    DONT_WANT_UPLOAD_PHOTO = 'Нет, не буду загружать свое фото 🙂'

    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=WANT_UPLOAD_PHOTO),
                KeyboardButton(text=DONT_WANT_UPLOAD_PHOTO)
            ]
        ],
        resize_keyboard=True,
    )