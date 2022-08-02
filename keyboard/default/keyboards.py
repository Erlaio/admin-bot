from aiogram.types import ReplyKeyboardMarkup

from pkg.db.department_func import get_all_departments
from .button_factory import ButtonFactory


class DepartmentsKeyboard(ButtonFactory):

    @classmethod
    async def __get_department(cls) -> None:
        all_departments = await get_all_departments()
        for department in all_departments:
            setattr(cls, department.department.upper(), department.department)

    @classmethod
    async def get_reply_keyboard(cls, one_time=False) -> ReplyKeyboardMarkup:
        await cls.__get_department()
        return super().get_reply_keyboard(one_time=one_time)


class AgreementKeyboard(ButtonFactory):
    AGREE_WITH_RULES = 'Я согласен с правилами 😎'
    DONT_AGREE_WITH_RULES = 'Я не согласен с правилами 🤔'


class CheckAccessKeyboard(ButtonFactory):
    CHECK_ACCESS = 'Проверить состояние анкеты ✅'


class ChoiceKeyboard(ButtonFactory):
    READ_RULES = 'Ознакомиться с правилами 🤓'
    DONT_READ_RULES = 'Я не буду читать правила 😐'


class DepartmentCommandsKeyboard(ButtonFactory):
    CREATE_DEPARTMENT = 'Создать новый отдел'
    DELETE_DEPARTMENT = 'Удалить отдел'
    CHANGE_DEPARTMENT_NAME = 'Сменить имя отдела'
    CHANGE_DEPARTMENT_LEAD = 'Сменить/добавить тим лида отдела'


class GenderKeyboard(ButtonFactory):
    MALE_GENDER = 'Мужской 👨'
    FEMALE_GENDER = 'Женский 👩‍🦰'


class PhotoKeyboard(ButtonFactory):
    WANT_UPLOAD_PHOTO = 'Да! Хочу загрузить свою фоточку 😎'
    DONT_WANT_UPLOAD_PHOTO = 'Нет, не буду загружать свое фото 🙂'


class ProjectCommandsKeyboard(ButtonFactory):
    CREATE_PROJECT = 'Создать новый проект'
    DELETE_PROJECT = 'Удалить проект'
    CHANGE_PROJECT_NAME = 'Сменить имя проекта'
    CHANGE_PROJECT_LEAD = 'Сменить/добавить тим лида проекта'


class ShowUserKeyboard(ButtonFactory):
    VIEW_ALL = 'Посмотреть всех'
    VIEW_ID = 'Посмотреть по ID'
    VIEW_TG_LOGIN = 'Посмотреть по Логину в Telegram'


class YesNoKeyboard(ButtonFactory):
    YES = 'Да ✅'
    NO = 'Нет ❌'
