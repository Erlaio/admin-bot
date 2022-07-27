import keyboard.default.keyboard


class ProjectCommands(keyboard.KeyboardFactory):
    KEYBOARD = ReplyKeyboardMarkup(resize_keyboard=True).row(
        KeyboardButton(text=button.CREATE_PROJECT),
        KeyboardButton(text=button.DELETE_PROJECT),
        KeyboardButton(text=button.CHANGE_PROJECT_NAME),
    ).insert(
        KeyboardButton(text=button.CHANGE_PROJECT_LEAD))
