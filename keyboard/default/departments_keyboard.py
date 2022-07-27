from keyboard.default import ButtonFactory
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from pkg.db.department_func import get_all_departments


class DepartmentsKeyboard(ButtonFactory):
    row_width = 5
    NO_DEPARTMENT = 'Без отдела'

    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=NO_DEPARTMENT)]],
        resize_keyboard=True,
    )

    @classmethod
    async def get_departments(cls):
        result = []
        for department in cls.KEYBOARD.keyboard[0]:
            result.append(department['text'])
        return result

    @classmethod
    async def add(cls, department_name: str):
        if await cls.is_exist(department_name):
            return None
        elif len(cls.KEYBOARD.keyboard[0]) % cls.row_width == 0:
            cls.KEYBOARD.insert(KeyboardButton(text=department_name))
        else:
            cls.KEYBOARD.row(KeyboardButton(text=department_name))

    departments_from_bd = get_all_departments()
    for counter, department in enumerate(departments_from_bd, start=1):
        KEYBOARD.keyboard[0].append(KeyboardButton(text=department.department))
        # if counter % row_width == 0:
        #     KEYBOARD.insert(KeyboardButton(text=department.department))
        # else:
        #     KEYBOARD.add(KeyboardButton(text=department.department))
