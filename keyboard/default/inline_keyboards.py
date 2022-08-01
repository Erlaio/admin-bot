from keyboard.default.button_factory import ButtonFactory


class ModeratorInlineKeyboard(ButtonFactory):

    def __init__(self, page, telegram_id):
        self.APPROVE = {'Одобрить': f'approve#{page}#{telegram_id}'}
        self.REFILLING = {'Перезаполнение': f'refilling#{page}#{telegram_id}'}
        self.DELETE = {'Удалить': f'delete_user#{page}#{telegram_id}'}
