import math
from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ButtonFactory(ABC):

    @classmethod
    def get_reply_keyboard(cls) -> ReplyKeyboardMarkup:
        key_list = [KeyboardButton(getattr(cls, i_const)) for i_const in dir(cls)[::-1] if i_const.isupper()]
        row = 3 if len(key_list) < 5 else math.ceil(len(key_list) / 2)
        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row).add(*key_list)

        return keyboard

    @classmethod
    def get_key_value(cls) -> dict:
        key_value = {i_const: getattr(cls, i_const) for i_const in dir(cls) if i_const.isupper()}

        return key_value
