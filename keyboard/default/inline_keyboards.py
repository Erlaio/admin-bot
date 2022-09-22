from keyboard.default.button_factory import ButtonFactory
from pkg.db.models.user import User


class ModeratorInlineKeyboard(ButtonFactory):

    def __init__(self, page, telegram_id, user_name, ):
        self.APPROVE = {
            'Одобрить': f'approve#{page}#{telegram_id}#{user_name}'}
        self.REFILLING = {
            'Перезаполнение': f'refilling#{page}#{telegram_id}#{user_name}'}
        self.DELETE = {
            'Удалить': f'delete_user#{page}#{telegram_id}#{user_name}'}


class BackInlineKeyboard(ButtonFactory):

    def __init__(self):
        self.BACK = {
            'Вернуться на главную': 'back'
        }


class ModeratorChangeCardInlineKeyboard(ButtonFactory):

    def __init__(self, page, user: User, ):
        self.SURNAME = {
            'Фамилия': f'change#{page}#surname#{user.telegram_id}'}
        self.NAME = {
            'Имя': f'change#{page}#name#{user.telegram_id}'}
        self.PATRONYMIC = {
            'Отчество': f'change#{page}#patronymic#{user.telegram_id}'}
        self.GENDER = {
            'Пол': f'change#{page}#gender#{user.telegram_id}'}
        self.TG_LOGIN = {
            'Логин в Telegram': f'change#{page}#tg_login#{user.telegram_id}'}
        self.DESIRED_DEPARTMENT = {
            'Отдел': f'change#{page}#desired_department#{user.telegram_id}'}
        self.SKILLS = {
            'Скилы': f'change#{page}#skills#{user.telegram_id}'}
        self.GOALS = {
            'Цели': f'change#{page}#goals#{user.telegram_id}'}
        self.CITY = {
            'Город': f'change#{page}#city#{user.telegram_id}'}
        self.SOURCE_OF_KNOWLEDGE = {
            'Откуда узнал о школе': f'change#{page}#source_of_knowledge#{user.telegram_id}'}
        self.LEAD_DESCRIPTION = {
            'Описание тимлида': f'change#{page}#lead_description#{user.telegram_id}'}
