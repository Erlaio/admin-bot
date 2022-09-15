import math
from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup


class ButtonFactory(ABC):
    __STOP_MESSAGE = 'Вернуться на главную'

    @classmethod
    def get_reply_keyboard(cls, add_stop=True,
                           one_time=False) -> ReplyKeyboardMarkup:
        key_list = [KeyboardButton(getattr(cls, i_const)) for i_const in dir(cls)[::-1]
                    if any([i_const.isupper(), i_const.isdigit()])]

        row = 3 if len(key_list) < 5 else math.ceil(len(key_list) / 5)

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

        return inline_keyboard

    @classmethod
    def get_stop_message(cls):
        return cls.__STOP_MESSAGE
