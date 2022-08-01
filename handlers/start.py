import imghdr
import os.path
import time

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, ContentType

from handlers.rules import RULES
from keyboard.default.inline_keyboards import ModeratorInlineKeyboard
from keyboard.default.keyboards import *
from loader import dp, bot
from pkg.db.user_func import *
from pkg.settings import settings
from states.start_state import StartState
from utils.config_utils import ConfigUtils
from utils.context_helper import ContextHelper
from utils.get_moder_chat_id import ModeratorUtils
from utils.get_name import get_fio
from utils.send_card import send_card


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = 'Приветствую! 👋 \nЭто телеграм бот "Школа IT". ' \
           'Чтобы продолжить наше общение, тебе нужно будет ' \
           'прочесть наши правила и согласиться с ними :)'
    await message.answer(text, reply_markup=ChoiceKeyboard.get_reply_keyboard())
    await StartState.rules.set()


@dp.message_handler(state=StartState.rules)
async def reading_rules(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == ChoiceKeyboard.READ_RULES:
        await message.answer(RULES, reply_markup=ReplyKeyboardRemove())
        await message.answer('Вы согласны с правилами?', reply_markup=AgreementKeyboard.get_reply_keyboard())
        await StartState.decision.set()
    elif answer == ChoiceKeyboard.DONT_READ_RULES:
        await message.answer(
            'Очень жаль что наше с тобой общение подходит к концу 😔\nЕсли же ты передумаешь,'
            'то я всегда тут)) Нужно лишь повторно вызвать команду /start',
            reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.rules.set()


@dp.message_handler(state=StartState.decision)
async def decision_about_rules(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == AgreementKeyboard.AGREE_WITH_RULES:
        if await get_user_by_tg_id(tg_id=message.from_user.id) is None:
            await message.answer('Введите ваше ФИО 🖊',
                                 reply_markup=ReplyKeyboardRemove())
            await StartState.gender.set()
        else:
            await message.answer('Вы уже зарегестрированы в системе. Хотите обновить данные?',
                                 reply_markup=YesNoKeyboard.get_reply_keyboard())
            await StartState.update_info.set()
    elif answer == AgreementKeyboard.DONT_AGREE_WITH_RULES:
        await message.answer('Жаль, что вас не устроили наши правила 😔\n'
                             'В любой момент, если передумаете, можете'
                             'попробовать снова, для этого нажмите команду /start',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision.set()


@dp.message_handler(state=StartState.update_info)
async def update_info(message: types.Message):
    answer = message.text
    if answer == YesNoKeyboard.YES:
        await message.answer('Введите ваше ФИО 🖊',
                             reply_markup=ReplyKeyboardRemove())
        tg_id = message.from_user.id
        await delete_user_by_tg_id(telegram_id=tg_id)
        await StartState.gender.set()
    elif answer == YesNoKeyboard.NO:
        await message.answer('Хотите проверить Вашу анкету?',
                             reply_markup=YesNoKeyboard.get_reply_keyboard())
        await StartState.choice.set()


@dp.message_handler(state=StartState.choice)
async def questionnaire_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == YesNoKeyboard.YES:
        await message.answer('Для проверки нажмите на кнопку ниже',
                             reply_markup=CheckAccessKeyboard.get_reply_keyboard())
        await StartState.check_questionnaire.set()
    elif answer == YesNoKeyboard.NO:
        await message.answer('Ок. Возвращаю Вас в начало',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()


@dp.message_handler(state=StartState.gender)
async def get_user_gender(message: types.Message, state: FSMContext):
    answer = message.text
    surname, name, patronymic = get_fio(answer)
    if name.isalpha():
        user = new_user()
        user.telegram_id = message.from_user.id
        user.tg_login = f"@{message.from_user.username}"
        user.surname, user.name, user.patronymic = surname, name, patronymic
        await add_new_user(user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите ваш пол',
                             reply_markup=GenderKeyboard.get_reply_keyboard())
        await StartState.photo.set()
    else:
        await message.answer('Необходимо ввести ФИО\nПример: Иванов Иван Иванович\n'
                             'Можно не указывать фамилию или отчество\nИмя указывать обязательно.')
        await StartState.gender.set()


@dp.message_handler(state=StartState.photo)
async def ask_about_photo(message: types.Message, state: FSMContext):
    answer = message.text
    message_text = 'Хотите ли вы загрузить свое фото?'
    user = await ContextHelper.get_user(state)
    if answer == GenderKeyboard.MALE_GENDER:
        user.gender = "Мужской"
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer(message_text,
                             reply_markup=PhotoKeyboard.get_reply_keyboard())
        await StartState.decision_about_photo.set()
    elif answer == GenderKeyboard.FEMALE_GENDER:
        user.gender = "Женский"
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer(message_text,
                             reply_markup=PhotoKeyboard.get_reply_keyboard())
        await StartState.decision_about_photo.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.photo.set()


@dp.message_handler(state=StartState.decision_about_photo)
async def decision_about_photo(message: types.Message):
    answer = message.text
    if answer == PhotoKeyboard.WANT_UPLOAD_PHOTO:
        await message.answer('Супер! Просто отправьте его мне.',
                             reply_markup=ReplyKeyboardRemove())
        await StartState.upload_photo.set()
    elif answer == PhotoKeyboard.DONT_WANT_UPLOAD_PHOTO:
        await message.answer('Хорошо, тогда продолжаем анкетирование 📝',
                             reply_markup=ReplyKeyboardRemove())
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
            await update_user_by_telegram_id(message.from_user.id, user)
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
    await update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите вашу ссылку на gitlab 🌐')
    await StartState.design.set()


@dp.message_handler(state=StartState.design)
async def design(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.git = answer
    await update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Вы дизайнер? 🎨', reply_markup=YesNoKeyboard.get_reply_keyboard())
    await StartState.decision_about_design.set()


@dp.message_handler(state=StartState.department)
async def get_department(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.desired_department = answer
    await update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите ваши навыки\n'
                         'Например: Python, Postgresql, Git, FastAPI, Django, '
                         'Go, aiogramm, asyncio',
                         reply_markup=ReplyKeyboardRemove())
    await StartState.goals.set()


@dp.message_handler(state=StartState.decision_about_design)
async def decision_about_design(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    if answer == YesNoKeyboard.YES:
        user.desired_department = 'Design'
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите вашу ссылку на беханс 🌐',
                             reply_markup=ReplyKeyboardRemove())
        await StartState.get_skills.set()
    elif answer == YesNoKeyboard.NO:
        await message.answer('В какой бы отдел Вы хотели попасть?',
                             reply_markup=await DepartmentsKeyboard.get_reply_keyboard())
        await StartState.department.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision_about_design.set()


@dp.message_handler(state=StartState.get_skills)
async def get_skills(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.behance = answer
    await update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите ваши навыки\n'
                         'Например: Python, Postgresql, Git, FastAPI, '
                         'Django, Go, aiogramm, asyncio')
    await StartState.goals.set()


@dp.message_handler(state=StartState.goals)
async def get_goals(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.skills = answer
    await update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Введите ваши цели\n'
                         '1. Основные ожидания от школы: ...\n2. '
                         'Вектор, куда ты хочешь развиваться:')
    await StartState.finish_questions.set()


@dp.message_handler(state=StartState.finish_questions)
async def finish_questions(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    user.goals = answer
    await update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer('Ваша анкета отправлена на проверку. '
                         'Пока ее не проверят функционал бота не доступен',
                         reply_markup=CheckAccessKeyboard.get_reply_keyboard())
    moder_chat_id = await ModeratorUtils().get_random_moder()
    await bot.send_message(chat_id=moder_chat_id, text='Йо проверь карту пж')
    await send_card(moder_chat_id, user,
                    reply_markup=ModeratorInlineKeyboard(page=1, user_id=user.user_id).get_inline_keyboard())
    await StartState.check_questionnaire.set()


@dp.message_handler(state=StartState.check_questionnaire)
async def check_questionnaire(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == CheckAccessKeyboard.CHECK_ACCESS:
        user = await get_user_by_tg_login(f'@{message.from_user.username}')
        if user.is_approved:
            await message.answer('Поздравляем\n\nСсылка на общий чат:\nhttps://t.me/+qGGF9z5Jy8MwMDA8',
                                 reply_markup=ReplyKeyboardRemove())
            await state.finish()
        else:
            await message.answer('Пока не одобрено',
                                 reply_markup=CheckAccessKeyboard.get_reply_keyboard())
            await StartState.check_questionnaire.set()
    elif answer == 'iammoder':
        await message.answer('Введите ключ доступа', reply_markup=ReplyKeyboardRemove())
        await StartState.get_moder.set()
    else:
        await message.answer('Чтобы проверить анкету нажмите на кнопку ниже',
                             reply_markup=CheckAccessKeyboard.get_reply_keyboard())
        await StartState.check_questionnaire.set()


@dp.message_handler(state=StartState.get_moder)
async def get_moder(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == settings.SECRET_KEY:
        await update_user_status(message.from_user.id)
        await message.answer('Ваша анкета одобрена и права модератора получены',
                             reply_markup=ReplyKeyboardRemove())
        await state.finish()
    else:
        await message.answer('Неверный ключ доступа')
        await StartState.check_questionnaire.set()
