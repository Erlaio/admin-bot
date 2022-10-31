import validators
from aiogram import types

from keyboard.default.keyboards import StopBotKeyboard
from pkg.db.user_func import get_user_by_tg_id


class Validations:

    def __init__(self, field_name: str, message: types.Message):
        self.field_name = field_name
        self.message = message

    async def validate_tg_login_email_git(self) -> bool:
        if self.field_name == 'tg_login':
            if self.message.text.startswith('@'):
                return True
            else:
                await self.message.answer(
                    'Пожалуйста, введите ваш логин с @\n(Например: @login)',
                    reply_markup=StopBotKeyboard.get_reply_keyboard())
                return False
        elif self.field_name == 'email':
            if validators.email(self.message.text):
                return True
            else:
                await self.message.answer('Вы ввели неверный формат почты',
                                          reply_markup=StopBotKeyboard.get_reply_keyboard())
                return False
        elif self.field_name == 'git' or self.field_name == 'behance':
            if validators.url(self.message.text):
                return True
            else:
                await self.message.answer(
                    'Введите, пожалуйста, корректную ссылку',
                    reply_markup=StopBotKeyboard.get_reply_keyboard())
                return False
        else:
            return True

    @staticmethod
    async def is_command(text: str) -> bool:
        if text.startswith('/'):
            return True
        return False

    @staticmethod
    async def moder_validation_for_supergroups(message: types.Message) -> bool:
        if message.chat.type == types.ChatType.SUPERGROUP:
            try:
                user = await get_user_by_tg_id(message.from_user.id)
                if user.is_moderator:
                    return True
                return False
            except Exception as e:
                print(e)
                return False
        else:
            return True

    @staticmethod
    async def length(text: str, minimum: int, maximum: int) -> bool:
        if validators.length(text, min=minimum, max=maximum):
            return False
        return True
