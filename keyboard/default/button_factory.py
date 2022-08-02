import math
from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


class ButtonFactory(ABC):

    @classmethod
    def get_reply_keyboard(cls, one_time=False) -> ReplyKeyboardMarkup:
        key_list = [KeyboardButton(getattr(cls, i_const)) for i_const in dir(cls)[::-1]
                    if any([i_const.isupper(), i_const.isdigit()])]

        row = 3 if len(key_list) < 5 else math.ceil(len(key_list) / 2)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row,
                                       one_time_keyboard=one_time).add(*key_list)

        return keyboard

    def get_inline_keyboard(self):
        key_list = self.__dict__

        inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True)

        for i_key in key_list.values():
            for j_key, j_value in i_key.items():
                inline_keyboard.insert(InlineKeyboardButton(text=j_key, callback_data=j_value))

        return inline_keyboard
