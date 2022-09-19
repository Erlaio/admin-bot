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
            'Фамилия': f'character_for_edit#{page}#surname#{user.surname}'}
        self.NAME = {
            'Имя': f'character_for_edit#{page}#name#{user.name}'}
        self.PATRONYMIC = {
            'Отчество': f'character_for_edit#{page}#patronymic#{user.patronymic}'}
        self.GENDER = {
            'Пол': f'character_for_edit#{page}#gender#{user.gender}'}
        self.TG_LOGIN = {
            'Логин в Telegram': f'character_for_edit#{page}#tg_login#{user.tg_login}'}
        self.DESIRED_DEPARTMENT = {
            'Отдел': f'character_for_edit#{page}#desired_department#{user.desired_department}'}
        self.SKILLS = {
            'Скилы': f'character_for_edit#{page}#skills#{user.skills}'}
        self.GOALS = {
            'Цели': f'character_for_edit#{page}#goals#{user.goals}'}
        self.CITY = {
            'Город': f'character_for_edit#{page}#city#{user.city}'}
        self.SOURCE_OF_KNOWLEDGE = {
            'Откуда узнал о школе': f'character_for_edit#{page}#source_of_knowledge#{user.source_of_knowledge}'}
        self.LEAD_DESCRIPTION = {
            'Описание тимлида': f'character_for_edit#{page}#lead_description#{user.lead_description}'}
