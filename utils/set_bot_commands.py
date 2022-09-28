from aiogram import types


async def set_default_commands(dp):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Запустить бота 💻'),
        types.BotCommand('help', 'Помощь 📣'),
        types.BotCommand('show_card', 'Показать карточку пользователя'),
        types.BotCommand(
            'show_department_cards',
            'Показать карточку пользователей отдела'),
        types.BotCommand('rules', 'Правила школы'),
        types.BotCommand('change_card', 'Изменение данных в своей карточке'),
        types.BotCommand('moder', 'Меню модератора')
    ])
