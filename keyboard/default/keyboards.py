from aiogram.types import ReplyKeyboardMarkup

from pkg.db.department_func import get_all_departments
from .button_factory import ButtonFactory


class StopBotKeyboard(ButtonFactory):
    STOP_BOT = 'Вернуться в начало'


class DepartmentsKeyboard(StopBotKeyboard):

    @classmethod
    async def __get_department(cls) -> None:
        all_departments = await get_all_departments()
        for department in all_departments:
            setattr(cls, department.department.upper(), department.department)

    @classmethod
    async def get_reply_keyboard(cls) -> ReplyKeyboardMarkup:
        await cls.__get_department()
        return super().get_reply_keyboard()


class AgreementKeyboard(StopBotKeyboard):
    AGREE_WITH_RULES = 'Я согласен с правилами 😎'
    DONT_AGREE_WITH_RULES = 'Я не согласен с правилами 🤔'


class CheckAccessKeyboard(ButtonFactory):           # TODO без stop
    CHECK_ACCESS = 'Проверить состояние анкеты ✅'


class ChoiceKeyboard(StopBotKeyboard):
    READ_RULES = 'Ознакомиться с правилами 🤓'
    DONT_READ_RULES = 'Я не буду читать правила 😐'


class DepartmentCommandsKeyboard(StopBotKeyboard):
    CREATE_DEPARTMENT = 'Создать новый отдел'
    DELETE_DEPARTMENT = 'Удалить отдел'
    CHANGE_DEPARTMENT_NAME = 'Сменить имя отдела'
    CHANGE_DEPARTMENT_LEAD = 'Сменить/добавить тим лида отдела'


class GenderKeyboard(StopBotKeyboard):
    MALE_GENDER = 'Мужской 👨'
    FEMALE_GENDER = 'Женский 👩‍🦰'


class PhotoKeyboard(StopBotKeyboard):
    WANT_UPLOAD_PHOTO = 'Да! Хочу загрузить свою фоточку 😎'
    DONT_WANT_UPLOAD_PHOTO = 'Нет, не буду загружать свое фото 🙂'


class ProjectCommandsKeyboard(StopBotKeyboard):
    CREATE_PROJECT = 'Создать новый проект'
    DELETE_PROJECT = 'Удалить проект'
    CHANGE_PROJECT_NAME = 'Сменить имя проекта'
    CHANGE_PROJECT_LEAD = 'Сменить/добавить тим лида проекта'


class ShowUserKeyboard(StopBotKeyboard):
    VIEW_ALL = 'Посмотреть всех'
    VIEW_ID = 'Посмотреть по ID'
    VIEW_TG_LOGIN = 'Посмотреть по Логину в Telegram'


class YesNoKeyboard(StopBotKeyboard):
    YES = 'Да ✅'
    NO = 'Нет ❌'
