from keyboard.default.button_factory import ButtonFactory


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
