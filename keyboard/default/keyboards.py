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
    async def get_reply_keyboard(cls, one_time=False, **kwargs) -> ReplyKeyboardMarkup:
        await cls.__get_department()
        return super().get_reply_keyboard(one_time=one_time)


class StopBotKeyboard(ButtonFactory):
    pass


class ChoiceKeyboard(ButtonFactory):
    B_READ_RULES = 'Ознакомиться с правилами 🤓'
    A_DONT_READ_RULES = 'Я не буду читать правила 😐'


class AgreementKeyboard(ButtonFactory):
    B_AGREE_WITH_RULES = 'Я согласен с правилами 😎'
    A_DONT_AGREE_WITH_RULES = 'Я не согласен с правилами 🤔'


class CheckAccessKeyboard(ButtonFactory):
    A_CHECK_ACCESS = 'Проверить состояние анкеты ✅'


class DepartmentCommandsKeyboard(ButtonFactory):
    D_CREATE_DEPARTMENT = 'Создать новый отдел'
    C_DELETE_DEPARTMENT = 'Удалить отдел'
    B_CHANGE_DEPARTMENT_NAME = 'Сменить имя отдела'
    A_CHANGE_DEPARTMENT_LEAD = 'Сменить/добавить тим лида отдела'


class GenderKeyboard(ButtonFactory):
    B_MALE_GENDER = 'Мужской 👨'
    A_FEMALE_GENDER = 'Женский 👩‍🦰'


class PhotoKeyboard(ButtonFactory):
    B_WANT_UPLOAD_PHOTO = 'Да! Хочу загрузить свою фоточку 😎'
    A_DONT_WANT_UPLOAD_PHOTO = 'Нет, не буду загружать свое фото 🙂'


class ProjectCommandsKeyboard(ButtonFactory):
    D_CREATE_PROJECT = 'Создать новый проект'
    C_DELETE_PROJECT = 'Удалить проект'
    B_CHANGE_PROJECT_NAME = 'Сменить имя проекта'
    A_CHANGE_PROJECT_LEAD = 'Сменить/добавить тим лида проекта'


class ShowUserKeyboard(ButtonFactory):
    C_VIEW_ALL = 'Посмотреть всех'
    B_VIEW_ID = 'Посмотреть по ID'
    A_VIEW_TG_LOGIN = 'Посмотреть по Логину в Telegram'


class YesNoKeyboard(ButtonFactory):
    B_YES = 'Да ✅'
    A_NO = 'Нет ❌'


class JoinedKeyboard(ButtonFactory):
    A_USER_JOINED = 'Я вступил!'
