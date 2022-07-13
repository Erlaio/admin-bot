from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Ознакомиться с правилами 🤓'),
            KeyboardButton(text='Я не буду читать правила 😐')
        ]
    ],
    resize_keyboard=True
)

agreement = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Я согласен с правилами 😎'),
            KeyboardButton(text='Я не согласен с правилами 🤔')
        ]
    ],
    resize_keyboard=True
)

gender = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Мужской 👨'),
            KeyboardButton(text='Женский 👩‍🦰')
        ]
    ],
    resize_keyboard=True
)

photo = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да! Хочу загрузить свою фоточку 😎'),
            KeyboardButton(text='Нет, не буду загружать свое фото 🙂')
        ]
    ],
    resize_keyboard=True
)

universal_choice = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Да ✅'),
            KeyboardButton(text='Нет ❌')
        ]
    ],
    resize_keyboard=True
)



