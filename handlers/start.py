import imghdr
import os.path
import typing
from pathlib import PurePath
import time

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, ContentType

from keyboard.default import button_value
from keyboard.default.button_value import ButtonValue as button
from keyboard.default.keyboard import *
from loader import dp, bot
from pkg.db.models.user import new_user
from pkg.db.user_func import add_new_user, update_user_by_telegram_id, get_user_by_tg_login, delete_user_by_tg_id, \
    get_user_by_tg_id, update_user_status
from pkg.settings import settings
from states.start_state import StartState
from utils.config_utils import ConfigUtils
from utils.context_helper import ContextHelper


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = 'Приветствую! 👋 \nЭто телеграм бот "Школа IT". Чтобы продолжить наше общение, тебе нужно будет ' \
           'прочесть наши правила и согласиться с ними :)'
    await message.answer(text, reply_markup=ChoiceKeyboard.CHOICE)
    await StartState.rules.set()


@dp.message_handler(state=StartState.rules)
async def reading_rules(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == button.READ_RULES:
        rules = 'Приветствуем в Школе IT!' \
                '\nДля того чтобы пройти дальше, нужно ознакомиться и согласиться с правилами Школы:\n\n' \
                "1. Еженедельные встречи.\n" \
                "Каждую пятницу с 19:00 - 20:00 проходят очные встречи для жителей Москвы, территориально, в десяти" \
                ' минутах от станции метро "Деловой центр".' \
                'Для жителей других городов, встречи проходят удалённо' \
                ' (нужно подключиться к звонку в общей беседе "Школа IT")\n\n' \
                '2. Личные карточки.\n' \
                'При вступлении в Школу необходимо заполнить личную карточку и отправить боту в дальнейшей беседе в' \
                ' этом чате.\n\n' \
                '3. Дедлайны\n' \
                'В Школе введена система передоговоров.' \
                'За день до дедлайна можно перенести дату.' \
                'Переносы обсуждаются с тимлидом направления.' \
                'Пример: дедлайн на задачу 18.07, передоговориться на по ней можно не позже 17.07.'
        await message.answer(rules, reply_markup=ReplyKeyboardRemove())
        await message.answer('Вы согласны с правилами?', reply_markup=AgreementKeyboard.AGREEMENT)
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
        if get_user_by_tg_id(tg_id=message.from_user.id) is None:
            await message.answer('Введите ваше ФИО 🖊', reply_markup=ReplyKeyboardRemove())
            await StartState.gender.set()
        else:
            await message.answer('Вы уже зарегестрированы в системе. Хотите обновить данные?',
                                 reply_markup=YesNoKeyboard.KEYBOARD)
            await StartState.update_info.set()
    elif answer == button.DONT_AGREE_WITH_RULES:
        await message.answer('Жаль, что вас не устроили наши правила 😔\nВ любой момент, если передумаете, можете'
                             'попробовать снова, для этого нажмите команду /start', reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision.set()


@dp.message_handler(state=StartState.update_info)
async def update_info(message: types.Message):
    answer = message.text
    if answer == button.YES:
        await message.answer('Введите ваше ФИО 🖊', reply_markup=ReplyKeyboardRemove())
        tg_id = message.from_user.id
        delete_user_by_tg_id(telegram_id=tg_id)
        await StartState.gender.set()
    elif answer == button.NO:
        await message.answer('Хотите проверить Вашу анкету?', reply_markup=YesNoKeyboard.KEYBOARD)
        await StartState.choise.set()


@dp.message_handler(state=StartState.choise)
async def choise(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == button.YES:
        await message.answer('Для проверки нажмите на кнопку ниже', reply_markup=CheckAccessKeyboard.KEYBOARD)
        await StartState.check_questionnaire.set()
    elif answer == button.NO:
        await message.answer('Ок. Возвращаю Вас в начало', reply_markup=ReplyKeyboardRemove())
        await state.reset_state()


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
    await message.answer('Введите ваш пол', reply_markup=GenderKeyboard.KEYBOARD)
    await StartState.photo.set()


@dp.message_handler(state=StartState.photo)
async def ask_about_photo(message: types.Message, state: FSMContext):
    answer = message.text
    message_text = 'Хотите ли вы загрузить свое фото?'
    reply_markup = PhotoKeyboard.KEYBOARD
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


@dp.message_handler(state=StartState.upload_photo, content_types=[ContentType.PHOTO, ContentType.DOCUMENT])
async def upload_photo(message: types.Message, state: FSMContext):
    timestamp = str(time.time()).replace(".", "")
    file_name = f"photo_{timestamp}.jpg"
    file_path = os.path.join(ConfigUtils.get_temp_path(), file_name)
    user = await ContextHelper.get_user(state)
    if not message.content_type == 'photo':
        file = await bot.get_file(message.document.file_id)
        await bot.download_file(file.file_path, file_path)
    else:
        await message.photo[-1].download(destination_file=file_path)
    with open(file_path, 'rb') as file:
        if not imghdr.what(file):
            await message.reply("Отправьте изображение.")
            await StartState.upload_photo.set()
        else:
            user.photo = file.read()
            update_user_by_telegram_id(message.from_user.id, user)
            await ContextHelper.add_user(user, state)
            await message.answer('Спасибо!')
            await message.answer('Введите вашу почту 📧')
            await StartState.gitlab.set()
    if os.path.exists(file_path):
        os.remove(file_path)


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
    await message.answer('Вы дизайнер? 🎨', reply_markup=YesNoKeyboard.KEYBOARD)
    await StartState.decision_about_design.set()


@dp.message_handler(state=StartState.department)
async def get_department(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.desired_department = answer
    update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите ваши навыки\n'
                         'Например: Python, Postgresql, Git, FastAPI, Django, Go, aiogramm, asyncio',
                         reply_markup=ReplyKeyboardRemove())
    await StartState.goals.set()


@dp.message_handler(state=StartState.decision_about_design)
async def decision_about_design(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    if answer == button.YES:
        user.desired_department = 'Design'
        update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите вашу ссылку на беханс 🌐', reply_markup=ReplyKeyboardRemove())
        await StartState.get_skills.set()
    elif answer == button.NO:
        await message.answer('В какой бы отдел Вы хотели попасть?',
                             reply_markup=DepartmentsKeyboard.KEYBOARD)
        await StartState.department.set()
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
    await message.answer('Введите ваши навыки\n'
                         'Например: Python, Postgresql, Git, FastAPI, Django, Go, aiogramm, asyncio')
    await StartState.goals.set()


@dp.message_handler(state=StartState.goals)
async def get_goals(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.skills = answer
    update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите ваши цели\n'
                         '1. Основные ожидания от школы: ...\n2. Вектор, куда ты хочешь развиваться:')
    await StartState.finish_questions.set()


@dp.message_handler(state=StartState.finish_questions)
async def finish_questions(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.goals = answer
    update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Ваша анкета отправлена на проверку. Пока ее не проверят функционал бота не доступен',
                         reply_markup=CheckAccessKeyboard.KEYBOARD)
    await StartState.check_questionnaire.set()


@dp.message_handler(state=StartState.check_questionnaire)
async def check_questionnaire(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == button.CHECK_ACCESS:
        user = get_user_by_tg_login(f'@{message.from_user.username}')
        if user.is_approved:
            await message.answer('Поздравляем', reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer('Пока не одобрено',
                                 reply_markup=CheckAccessKeyboard.KEYBOARD)
            await StartState.check_questionnaire.set()
    elif answer == 'iammoder':
        await message.answer('Введите ключ доступа', reply_markup=ReplyKeyboardRemove())
        await StartState.get_moder.set()
    else:
        await message.answer('Чтобы проверить анкету нажмите на кнопку ниже',
                             reply_markup=CheckAccessKeyboard.KEYBOARD)
        await StartState.check_questionnaire.set()


@dp.message_handler(state=StartState.get_moder)
async def get_moder(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == settings.SECRET_KEY:
        update_user_status(message.from_user.id)
        await message.answer('Ваша анкета одобрена и права модератора получены', reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer('Неверный ключ доступа')
        await StartState.check_questionnaire.set()
