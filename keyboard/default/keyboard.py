from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


class ButtonFactory:
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[[]],
        resize_keyboard=True,
    )

    @classmethod
    async def delete(cls, department_name: str):
        if await cls.is_exist(department_name):
            cls.KEYBOARD.keyboard[0].remove(KeyboardButton(text=department_name))
        else:
            return None

    @classmethod
    async def rename(cls, old_name: str, new_name: str):
        for index, department in enumerate(cls.KEYBOARD.keyboard[0]):
            if old_name in department['text']:
                department[index]['text'] = new_name
                return
        else:
            return None

    @classmethod
    async def is_exist(cls, department_name: str):
        for index, department in enumerate(cls.KEYBOARD.keyboard[0]):
            if department_name in department['text']:
                return True
        else:
            return False
