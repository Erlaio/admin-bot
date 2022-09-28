import math
from abc import ABC
from typing import List

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


class ButtonFactory(ABC):
    __STOP_MESSAGE = 'Вернуться на главную'

    @classmethod
    def get_reply_keyboard(cls, add_stop=True,
                           one_time=False) -> ReplyKeyboardMarkup:
        key_list = [KeyboardButton(getattr(cls, i_const)) for i_const in dir(cls)
                    if any([i_const.isupper(), i_const.isdigit()])]

        row = 3 if len(key_list) < 6 else math.ceil(len(key_list) / 4)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row,
                                       one_time_keyboard=one_time).add(*key_list)

        if add_stop:
            keyboard.row(KeyboardButton(cls.__STOP_MESSAGE))

        return keyboard

    def get_inline_keyboard(self, is_key=False):
        key_list = self.__dict__

        if is_key:
            inline_keyboard = []

            for i_key in key_list.values():
                for j_key, j_value in i_key.items():
                    inline_keyboard.append(
                        InlineKeyboardButton(
                            text=j_key, callback_data=j_value))
        else:
            inline_keyboard = InlineKeyboardMarkup(resize_keyboard=True)

            for i_key in key_list.values():
                for j_key, j_value in i_key.items():
                    inline_keyboard.insert(
                        InlineKeyboardButton(
                            text=j_key, callback_data=j_value))

        try:
            if len(inline_keyboard) == any(inline_keyboard_len for inline_keyboard_len in range(1, 4)):
                return inline_keyboard
        finally:
            if not any(isinstance(inline_keyboard, list) for _ in inline_keyboard):
                return inline_keyboard

        upd_inline_keyboard = []
        index = 0
        for _ in range(math.ceil(len(inline_keyboard) / 3)):
            upd_inline_keyboard.append(inline_keyboard[index:index + 3])
            index += 3
        return upd_inline_keyboard

    @classmethod
    def get_stop_message(cls):
        return cls.__STOP_MESSAGE
