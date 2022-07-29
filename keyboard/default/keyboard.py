from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboard.default.button_value import ButtonValue as button
from pkg.db.department_func import get_all_departments


class Keyboard:
    CHOICE = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.READ_RULES),
                KeyboardButton(text=button.DONT_READ_RULES)
            ]
        ],
        resize_keyboard=True
    )

    AGREEMENT = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.AGREE_WITH_RULES),
                KeyboardButton(text=button.DONT_AGREE_WITH_RULES)
            ]
        ],
        resize_keyboard=True
    )

    GENDER = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.MALE_GENDER),
                KeyboardButton(text=button.FEMALE_GENDER)
            ]
        ],
        resize_keyboard=True
    )

    PHOTO = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.WANT_UPLOAD_PHOTO),
                KeyboardButton(text=button.DONT_WANT_UPLOAD_PHOTO)
            ]
        ],
        resize_keyboard=True
    )

    UNIVERSAL_CHOICE = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.YES),
                KeyboardButton(text=button.NO)
            ]
        ],
        resize_keyboard=True
    )

    CHECK_ACCESS = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.CHECK_ACCESS),
            ]
        ],
        resize_keyboard=True
    )

    # DEPARTMENTS = ReplyKeyboardMarkup(            # useless for now
    #     keyboard=[
    #         [
    #             KeyboardButton(text=button.FRONTEND),
    #             KeyboardButton(text=button.BACKEND),
    #             KeyboardButton(text=button.ML),
    #             KeyboardButton(text=button.DS),
    #             KeyboardButton(text=button.DESIGN),
    #             KeyboardButton(text=button.MOBILE_DEVELOPMENT),
    #         ]
    #     ],
    #     resize_keyboard=True
    # )

    SHOW_USER = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.VIEW_ALL),
                KeyboardButton(text=button.VIEW_ID),
                KeyboardButton(text=button.VIEW_TG_LOGIN)
            ]
        ],
        resize_keyboard=True
    )

    DEPARTMENTS_COMMANDS = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(text=button.CREATE_DEPARTMENT),
        KeyboardButton(text=button.DELETE_DEPARTMENT),
        KeyboardButton(text=button.CHANGE_DEPARTMENT_NAME)
    ).insert(
        KeyboardButton(text=button.CHANGE_DEPARTMENT_LEAD)
    )

    PROJECTS_COMMANDS = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(text=button.CREATE_PROJECT),
        KeyboardButton(text=button.DELETE_PROJECT),
        KeyboardButton(text=button.CHANGE_PROJECT_NAME)
    ).insert(
        KeyboardButton(text=button.CHANGE_PROJECT_LEAD)
    )


class DepartmentButtonFactory:
    DEPARTMENTS = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[[KeyboardButton(text='Без отдела')]],
    )

    @classmethod
    async def read_departments(cls):
        departments_from_bd = await get_all_departments()
        for department in departments_from_bd:
            cls.DEPARTMENTS.keyboard[0].append(KeyboardButton(text=department.department))
        return

    @classmethod
    async def delete(cls, department_name: str):
        if await cls.is_exist(department_name):
            cls.DEPARTMENTS.keyboard[0].remove(KeyboardButton(text=department_name))
        else:
            return None

    @classmethod
    async def rename(cls, old_name: str, new_name: str):
        for index, department in enumerate(cls.DEPARTMENTS.keyboard[0]):
            if old_name in department['text']:
                department[index]['text'] = new_name
                return
        else:
            return None

    @classmethod
    async def add(cls, department_name: str):
        if await cls.is_exist(department_name):
            return None
        else:
            cls.DEPARTMENTS.keyboard[0].append(KeyboardButton(text=department_name))

    @classmethod
    async def is_exist(cls, department_name: str):
        for index, department in enumerate(cls.DEPARTMENTS.keyboard[0]):
            if department_name in department['text']:
                return True
        else:
            return False

    @classmethod
    async def get_departments(cls):
        result = []
        for department in cls.DEPARTMENTS.keyboard[0]:
            result.append(department['text'])
        return result
