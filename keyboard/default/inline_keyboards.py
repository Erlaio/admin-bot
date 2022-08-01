from keyboard.default.button_factory import ButtonFactory


class ModeratorInlineKeyboard(ButtonFactory):

    def __init__(self, page, user_id):
        self.APPROVE = {'Одобрить': f'approve#{page}#{user_id}'}
        self.REFILLING = {'Перезаполнение': f'refilling#{page}#{user_id}'}
        self.DELETE = {'Удалить': f'delete_user#{page}#{user_id}'}
