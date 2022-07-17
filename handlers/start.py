import os.path
from pathlib import PurePath
import time

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove

from keyboard.default.button_value import ButtonValue as button
from keyboard.default.keyboard import Keyboard
from loader import dp
from pkg.db.models.user import new_user
from pkg.db.user_func import add_new_user, update_user_by_telegram_id
from states.start_state import StartState
from utils.config_utils import ConfigUtils
from utils.context_helper import ContextHelper

from pkg.db.department_func import get_users_from_department


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = 'Приветствую! 👋 \nЭто телеграм бот "Школа IT". Чтобы продолжить наше общение, тебе нужно будет' \
           'прочесть наши правила и согласиться с ними :)'
    await message.answer(text, reply_markup=Keyboard.CHOICE)
    await StartState.rules.set()


@dp.message_handler(state=StartState.rules)
async def reading_rules(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == button.READ_RULES:
        await message.answer('Тут говорится о правилах.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Вы согласны с правилами?', reply_markup=Keyboard.AGREEMENT)
        await StartState.decision.set()
    elif answer == button.DONT_READ_RULES:
        await message.answer('Очень жаль что наше с тобой общение подходит к концу 😔\nЕсли же ты передумаешь,'
                             'то я всегда тут)) Нужно лишь повторно вызвать команду /start',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.rules.set()


@dp.message_handler(state=StartState.decision)
async def decision_about_rules(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == button.AGREE_WITH_RULES:
        await message.answer('Введите ваше ФИО 🖊', reply_markup=ReplyKeyboardRemove())
        await StartState.gender.set()
    elif answer == button.DONT_AGREE_WITH_RULES:
        await message.answer('Жаль, что вас не устроили наши правила 😔\nВ любой момент, если передумаете, можете'
                             'попробовать снова, для этого нажмите команду /start', reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision.set()


@dp.message_handler(state=StartState.gender)
async def get_user_gender(message: types.Message, state: FSMContext):
    answer = message.text
    splitted_full_name = answer.split(" ")
    user = new_user()
    user.telegram_id = message.from_user.id
    user.tg_login = f"@{message.from_user.username}"
    user.surname = splitted_full_name[0]
    try:
        user.name = splitted_full_name[1]
    except IndexError:
        user.name = ""
    try:
        user.patronymic = splitted_full_name[2]
    except IndexError:
        user.patronymic = ""
    add_new_user(user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите ваш пол', reply_markup=Keyboard.GENDER)
    await StartState.photo.set()


@dp.message_handler(state=StartState.photo)
async def ask_about_photo(message: types.Message, state: FSMContext):
    answer = message.text
    message_text = 'Хотите ли вы загрузить свое фото?'
    reply_markup = Keyboard.PHOTO
    user = await ContextHelper.get_user(state)
    if answer == button.MALE_GENDER:
        user.gender = "Мужской"
        update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer(message_text, reply_markup=reply_markup)
        await StartState.decision_about_photo.set()
    elif answer == button.FEMALE_GENDER:
        user.gender = "Женский"
        update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer(message_text, reply_markup=reply_markup)
        await StartState.decision_about_photo.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.photo.set()


@dp.message_handler(state=StartState.decision_about_photo)
async def decision_about_photo(message: types.Message):
    answer = message.text
    if answer == button.WANT_UPLOAD_PHOTO:
        await message.answer('Супер! Просто отправьте его мне.', reply_markup=ReplyKeyboardRemove())
        await StartState.upload_photo.set()
    elif answer == button.DONT_WANT_UPLOAD_PHOTO:
        await message.answer('Хорошо, тогда продолжаем анкетирование 📝', reply_markup=ReplyKeyboardRemove())
        await message.answer('Введите вашу почту 📧')
        await StartState.gitlab.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision_about_photo.set()


@dp.message_handler(state=StartState.upload_photo, content_types=["photo"])
async def upload_photo(message: types.Message, state: FSMContext):
    timestamp = str(time.time()).replace(".", "")
    file_name = f"photo_{timestamp}.jpg"
    file_path = str(PurePath(ConfigUtils.get_project_root(), "temp", file_name))
    user = await ContextHelper.get_user(state)
    await message.photo[-1].download(destination_file=file_path)
    with open(file_path, 'rb') as file:
        user.photo = file.read()
        update_user_by_telegram_id(message.from_user.id, user)
    if os.path.exists(file_path):
        os.remove(file_path)
    await ContextHelper.add_user(user, state)
    await message.answer('Спасибо!')
    await message.answer('Введите вашу почту 📧')
    await StartState.gitlab.set()


@dp.message_handler(state=StartState.gitlab)
async def get_gitlab(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.email = answer
    update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите вашу ссылку на gitlab 🌐')
    await StartState.design.set()


@dp.message_handler(state=StartState.design)
async def design(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.git = answer
    update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Вы дизайнер? 🎨', reply_markup=Keyboard.UNIVERSAL_CHOICE)
    await StartState.decision_about_design.set()


@dp.message_handler(state=StartState.decision_about_design)
async def decision_about_design(message: types.Message):
    answer = message.text
    if answer == button.YES:
        await message.answer('Введите вашу ссылку на беханс 🌐', reply_markup=ReplyKeyboardRemove())
        await StartState.get_skills.set()
    elif answer == button.NO:
        await message.answer('Введите ваши навыки\nТут нужно будет добавить '
                             'шаблон', reply_markup=ReplyKeyboardRemove())
        await StartState.goals.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision_about_design.set()


@dp.message_handler(state=StartState.get_skills)
async def get_skills(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.behance = answer
    update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите ваши навыки\nТут нужно будет добавить шаблон')
    await StartState.goals.set()


@dp.message_handler(state=StartState.goals)
async def get_goals(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.skills = answer
    update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите ваши цели\nТут нужно будет добавить шаблон')
    await StartState.finish_questions.set()


@dp.message_handler(state=StartState.finish_questions)
async def finish_questions(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.goals = answer
    update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Ваша анкета отправлена на проверку. Пока ее не проверят функционал бота не доступен',
                         reply_markup=Keyboard.CHECK_ACCESS)
    await StartState.check_questionnaire.set()


@dp.message_handler(state=StartState.check_questionnaire)
async def check_questionnaire(message: types.Message):
    answer = message.text
    if answer == button.CHECK_ACCESS:
        pass
    else:
        await message.answer('Чтобы проверить анкету нажмите на кнопку ниже')
        await StartState.departments.set()


@dp.message_handler(state=StartState.departments)
async def output_users_by_department(message: types.Message):
    await message.answer(text='Выберите отдел для вывода', reply_markup=Keyboard.DEPARTMENTS)
    answer = message.text
    if answer == button.FRONTEND:
        data = get_users_from_department(1)
    elif answer == button.BACKEND:
        data = get_users_from_department(2)
    elif answer == button.ML:
        data = get_users_from_department(3)
    elif answer == button.DS:
        data = get_users_from_department(4)
    elif answer == button.DESIGN:
        data = get_users_from_department(5)
    elif answer == button.MOBILE_DEVELOPMENT:
        data = get_users_from_department(6)
    for field in data:                          # Не уверен, что это адекватное решение. Вдруг появятся идеи
        await message.answer(
            f"ID: {field[0]}\n"
            f"Фамилия: {field[1]}\n"
            f"Имя: {field[2]}\n"
            f"Отчество: {field[3]}\n"
            f"Пол: {field[4]}\n"
            # f"Фото: {field[5]}\n"
            f"Почта: {field[6]}\n"
            f"Гит: {field[7]}\n"
            f"Телеграм: {field[8]}\n"
            f"Желаемый отдел: {field[9]}\n"
            f"Скилы: {field[10]}\n"
            f"Цели: {field[11]}\n"
            f"Описание лида: {field[12]}\n"
            f"Время присоединения: {field[13]}\n"
            f"Является модератором: {field[14]}\n"
            f"Принят: {field[15]}",
            reply_markup=ReplyKeyboardRemove()
        )
    else:
        pass            # Обработать TypeError

