import math
from abc import ABC

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ButtonFactory(ABC):

    @classmethod
    def get_reply_keyboard(cls) -> ReplyKeyboardMarkup:
        key_list = [KeyboardButton(getattr(cls, i_const)) for i_const in dir(cls)[::-1]
                    if i_const != 'STOP_BOT' and any([i_const.isupper(), i_const.isdigit()])]
        stop_button = [KeyboardButton(getattr(cls, i_const)) for i_const in dir(cls) if i_const == 'STOP_BOT']

        row = 3 if len(key_list) < 5 else math.ceil(len(key_list) / 2)

        keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row).add(*key_list)
        keyboard.add(*stop_button)

        return keyboard
