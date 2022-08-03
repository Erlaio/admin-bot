import math
from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ButtonFactory(ABC):

    @classmethod
    def get_reply_keyboard(cls, add_stop=True, one_time=False) -> ReplyKeyboardMarkup:
        key_list = [KeyboardButton(getattr(cls, i_const)) for i_const in dir(cls)[::-1]
                    if any([i_const.isupper(), i_const.isdigit()])]

        row = 3 if len(key_list) < 5 else math.ceil(len(key_list) / 2)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row).add(*key_list)

        if add_stop:
            keyboard.row(KeyboardButton('Вернуться на главную'))

        return keyboard
