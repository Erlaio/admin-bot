from aiogram.dispatcher.filters.state import StatesGroup, State


class StartState(StatesGroup):
    rules = State()
    decision = State()
    user_name = State()
    gender = State()
    photo = State()
    email = State()
    decision_about_photo = State()
    upload_photo = State()
    gitlab = State()
    department = State()
    design = State()
    decision_about_design = State()
    get_skills = State()
    goals = State()
    finish_questions = State()
    check_questionnaire = State()
    update_info = State()
    choise = State()
