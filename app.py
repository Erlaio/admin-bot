from utils.set_bot_commands import set_default_commands
from pkg.db.department_func import get_all_departments

Departments = []


async def on_startup(dp):
    print("Start Bot")
    global Departments
    Departments = await get_all_departments()
    print(Departments)
    await set_default_commands(dp)


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup)
