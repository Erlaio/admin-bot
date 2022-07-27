from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from keyboard.default.button_value import ButtonValue as button
from pkg.db.department_func import get_all_departments


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


class DepartmentsKeyboard(ButtonFactory):
    row_width = 5
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text='Без отдела')]],
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


class ChoiceKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=button.READ_RULES),
             KeyboardButton(text=button.READ_RULES)]
        ],
        resize_keyboard=True,
    )


class AgreementKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=button.AGREE_WITH_RULES),
             KeyboardButton(text=button.DONT_AGREE_WITH_RULES)]
        ],
        resize_keyboard=True,
    )


class GenderKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(

        keyboard=[
            [KeyboardButton(text=button.MALE_GENDER),
             KeyboardButton(text=button.FEMALE_GENDER)]
        ],
        resize_keyboard=True,
    )


class PhotoKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.WANT_UPLOAD_PHOTO),
                KeyboardButton(text=button.DONT_WANT_UPLOAD_PHOTO)
            ]
        ],
        resize_keyboard=True,
    )


class YesNoKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.YES),
                KeyboardButton(text=button.NO)
            ]
        ],
        resize_keyboard=True
    )


class CheckAccessKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.CHECK_ACCESS),
            ]
        ],
        resize_keyboard=True
    )


class ShowUserKeyboard(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=button.VIEW_ALL),
                KeyboardButton(text=button.VIEW_ID),
                KeyboardButton(text=button.VIEW_TG_LOGIN)
            ]
        ],
        resize_keyboard=True
    )


class DepartmentCommands(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3).row(
        KeyboardButton(text=button.CREATE_DEPARTMENT),
        KeyboardButton(text=button.DELETE_DEPARTMENT),
        KeyboardButton(text=button.CHANGE_DEPARTMENT_NAME)).insert(
        KeyboardButton(text=button.CHANGE_DEPARTMENT_NAME))


class ProjectCommands(ButtonFactory):
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(text=button.CREATE_PROJECT),
        KeyboardButton(text=button.DELETE_PROJECT),
        KeyboardButton(text=button.CHANGE_PROJECT_NAME),
    ).insert(
        KeyboardButton(text=button.CHANGE_PROJECT_LEAD))
