from aiogram.dispatcher.filters.state import StatesGroup, State


class UserCardState(StatesGroup):
    show_user_choice = State()
    user_id = State()
