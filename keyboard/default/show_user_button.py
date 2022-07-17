from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

show_user = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Посмотреть всех'),
            KeyboardButton(text='Посмотреть конкретного')
        ]
    ],
    resize_keyboard=True
)
