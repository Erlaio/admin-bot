import imghdr
import os.path
import time

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove, ContentType
from pydantic.error_wrappers import ValidationError

from handlers.rules import RULES
from keyboard.default.inline_keyboards import ModeratorInlineKeyboard
from keyboard.default.keyboards import *
from loader import dp, bot
from pkg.db.user_func import *
from pkg.settings import settings
from states.start_state import StartState
from utils.config_utils import ConfigUtils
from utils.context_helper import ContextHelper
from utils.get_name import split_fullname
from utils.send_card import send_card
from utils.delete_user import delete_user


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = 'Привет! ' \
           'Рады тебя приветствовать в Школе IT! ' \
           '\nШкола IT Terra создана для помощи благотворительным фондам и людям.' \
           ' Каждый участник вносит вклад в общее дело. ' \
           'Школа – это комьюнити, которое помогает прокачивать навыки всем желающим. Мы учимся новому и всегда ' \
           'готовы помочь каждому участнику разобраться с возникшим вопросом.  ' \
           '\nЗдесь собрались самые любознательные, целеустремленные и приветливые люди.' \
           ' Мы объединяем новичков и специалистов разных возрастов не только из разных городов России, но и стран. ' \
           '\nДля того, чтобы попасть в Школу просим ответить на несколько вопросов…'
    await message.answer(text, reply_markup=ChoiceKeyboard.get_reply_keyboard())
    await StartState.rules.set()


@dp.message_handler(commands='stop', state='*')
@dp.message_handler(Text(equals=ButtonFactory.get_stop_message()), state='*')
async def bot_stop(message: types.Message, state: FSMContext):
    text = 'Главная страница'
    await message.answer(text, reply_markup=types.ReplyKeyboardRemove())
    await state.finish()


@dp.message_handler(commands='iammoder')
async def get_moder(message: types.Message):
    await message.answer('Введите ключ доступа', reply_markup=StopBotKeyboard.get_reply_keyboard())
    await StartState.get_moder.set()


@dp.message_handler(state=StartState.rules_for_refilling)
async def get_rules(message: types.Message):
    text = 'Чтобы перезаполнить анкету, напомним правила :)'
    await message.answer(text, reply_markup=ChoiceKeyboard.get_reply_keyboard())
    await StartState.rules.set()


@dp.message_handler(state=StartState.rules)
async def reading_rules(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == ChoiceKeyboard.B_READ_RULES:
        await message.answer(RULES, reply_markup=ReplyKeyboardRemove())
        await message.answer('Вы согласны с правилами?', reply_markup=AgreementKeyboard.get_reply_keyboard())
        await StartState.decision.set()
    elif answer == ChoiceKeyboard.A_DONT_READ_RULES:
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
    if answer == AgreementKeyboard.B_AGREE_WITH_RULES:
        if await get_user_by_tg_id(tg_id=message.from_user.id) is None:
            await message.answer('Введите ваше ФИО 🖊',
                                 reply_markup=StopBotKeyboard.get_reply_keyboard())
            await StartState.gender.set()
        else:
            await message.answer('Вы уже зарегистрированы в системе. Хотите обновить данные?',
                                 reply_markup=YesNoKeyboard.get_reply_keyboard())
            await StartState.update_info.set()
    elif answer == AgreementKeyboard.A_DONT_AGREE_WITH_RULES:
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
    if answer == YesNoKeyboard.B_YES:
        await message.answer('Введите ваше ФИО 🖊',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        tg_id = message.from_user.id
        await delete_user_by_tg_id(telegram_id=tg_id)
        await StartState.gender.set()
    elif answer == YesNoKeyboard.A_NO:
        await message.answer('Хотите проверить Вашу анкету?',
                             reply_markup=YesNoKeyboard.get_reply_keyboard())
        await StartState.choice.set()


@dp.message_handler(state=StartState.choice)
async def questionnaire_choice(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == YesNoKeyboard.B_YES:
        await message.answer('Для проверки нажмите на кнопку ниже',
                             reply_markup=CheckAccessKeyboard.get_reply_keyboard(add_stop=False))
        await StartState.check_questionnaire.set()
    elif answer == YesNoKeyboard.A_NO:
        await message.answer('Ок. Возвращаю Вас в начало',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()


@dp.message_handler(state=StartState.gender)
async def get_user_gender(message: types.Message, state: FSMContext):
    answer = message.text
    surname, name, patronymic = split_fullname(answer)
    if name.isalpha():
        user = User()
        user.telegram_id = message.from_user.id
        user.tg_login = f'@{message.from_user.username}'
        user.surname, user.name, user.patronymic = surname, name, patronymic
        await add_new_user(user)
        await ContextHelper.add_user(user, state)
        await message.answer('Выберите ваш пол',
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
    if answer == GenderKeyboard.B_MALE_GENDER:
        user.gender = 'Мужской'
    elif answer == GenderKeyboard.A_FEMALE_GENDER:
        user.gender = 'Женский'
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.photo.set()
        return
    await update_user_by_telegram_id(message.from_user.id, user)
    await ContextHelper.add_user(user, state)
    await message.answer(message_text,
                         reply_markup=PhotoKeyboard.get_reply_keyboard())
    await StartState.decision_about_photo.set()


@dp.message_handler(state=StartState.decision_about_photo)
async def decision_about_photo(message: types.Message):
    answer = message.text
    if answer == PhotoKeyboard.B_WANT_UPLOAD_PHOTO:
        await message.answer('Супер! Просто отправьте его мне.',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.upload_photo.set()
    elif answer == PhotoKeyboard.A_DONT_WANT_UPLOAD_PHOTO:
        await message.answer('Хорошо, тогда продолжаем анкетирование 📝',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await message.answer('Введите вашу почту 📧')
        await StartState.gitlab.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision_about_photo.set()


@dp.message_handler(state=StartState.upload_photo,
                    content_types=[ContentType.PHOTO, ContentType.DOCUMENT])
async def upload_photo(message: types.Message, state: FSMContext):
    timestamp = str(time.time()).replace('.', '')
    file_name = f'photo_{timestamp}.jpg'
    file_path = os.path.join(ConfigUtils.get_temp_path(), file_name)
    user = await ContextHelper.get_user(state)
    if not message.content_type == 'photo':
        file = await bot.get_file(message.document.file_id)
        await bot.download_file(file.file_path, file_path)
    else:
        await message.photo[-1].download(destination_file=file_path)
    with open(file_path, 'rb') as file:
        if not imghdr.what(file):
            await message.reply('Отправьте изображение.', reply_markup=StopBotKeyboard.get_reply_keyboard())
            await StartState.upload_photo.set()
        else:
            user.photo = file.read()
            await update_user_by_telegram_id(message.from_user.id, user)
            await ContextHelper.add_user(user, state)
            await message.answer('Спасибо!')
            await message.answer('Введите вашу почту 📧', reply_markup=StopBotKeyboard.get_reply_keyboard())
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
    await message.answer('Введите вашу ссылку на gitlab 🌐',
                         reply_markup=StopBotKeyboard.get_reply_keyboard())
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
                         reply_markup=StopBotKeyboard.get_reply_keyboard())
    await StartState.goals.set()


@dp.message_handler(state=StartState.decision_about_design)
async def decision_about_design(message: types.Message, state: FSMContext):
    answer = message.text
    user = await ContextHelper.get_user(state)
    if answer == YesNoKeyboard.B_YES:
        user.desired_department = 'Design'
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите вашу ссылку на беханс 🌐',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.get_skills.set()
    elif answer == YesNoKeyboard.A_NO:
        await message.answer('Выберите, в какой бы отдел Вы хотели попасть?',
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
                         'Django, Go, aiogramm, asyncio', reply_markup=StopBotKeyboard.get_reply_keyboard())
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
                         'Вектор, куда ты хочешь развиваться:',
                         reply_markup=StopBotKeyboard.get_reply_keyboard())
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
                         reply_markup=CheckAccessKeyboard.get_reply_keyboard(add_stop=False))
    # moder_chat_id = await ModeratorUtils().get_random_moder()         # функционал для отправки модеру в личку
    await bot.send_message(chat_id=settings.TELEGRAM_MODERS_CHAT_ID, text=f'Пришла карточка {user.tg_login}')
    await send_card(chat_id=settings.TELEGRAM_MODERS_CHAT_ID, user=user,
                    reply_markup=ModeratorInlineKeyboard(
                        page=0,
                        telegram_id=user.telegram_id,
                        user_name=user.tg_login
                    ).get_inline_keyboard())
    await StartState.check_questionnaire.set()


@dp.message_handler(state=StartState.check_questionnaire)
async def check_questionnaire(message: types.Message):
    # channels = settings.TELEGRAM_SCHOOL_CHATS
    answer = message.text
    if answer == CheckAccessKeyboard.A_CHECK_ACCESS:
        try:
            user = await get_user_by_tg_login(f'@{message.from_user.username}')
            if user.is_approved:
                # formatted_channels = ' '.join(map(str, channels))
                text = 'Анкета одобрена, поздравляем!\n\nТебе необходимо вступить во все ' \
                       'следующие группы в течение 2 дней:\n{}\n'. \
                    format('Школа IT:\nhttps://t.me/+qGGF9z5Jy8MwMDA8'
                           '\n\nПроекты:\nhttps://t.me/+HwhF6emf-asxYmMy')
                await message.answer(text,
                                     reply_markup=JoinedKeyboard.get_reply_keyboard(add_stop=False))
                await StartState.check_membership.set()
            else:
                await message.answer('Пока не одобрено',
                                     reply_markup=CheckAccessKeyboard.get_reply_keyboard(add_stop=False))
        except ValidationError:
            await bot.send_message(chat_id=message.chat.id,
                                   text='Неверно заполнена анкета, заполните как в примере')
            moder = await get_random_moder()
            await send_card(message.chat.id, moder)
            await bot.send_message(chat_id=message.chat.id,
                                   text='Для перезаполнения анкеты нажмите на кнопку ниже',
                                   reply_markup=MoveToRefilling.get_reply_keyboard(add_stop=False))
            await StartState.rules_for_refilling.set()
    else:
        await message.answer('Чтобы проверить анкету нажмите на кнопку ниже',
                             reply_markup=CheckAccessKeyboard.get_reply_keyboard(add_stop=False))
        await StartState.check_questionnaire.set()


@dp.message_handler(state=StartState.check_membership)
async def check_membership(message: types.Message, state: FSMContext):
    is_member = True
    channels = settings.TELEGRAM_SCHOOL_CHATS
    is_first_check = True
    user_id = message.from_user.id

    while True:
        for channel in channels:
            user_status = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if user_status.status == 'kicked':
                await message.answer('Вы заблокированы в одном из наших чатов. '
                                     'Обратитесь к тимлиду или модератору',
                                     reply_markup=ReplyKeyboardRemove())
                await delete_user(user_id, channels)
                await state.finish()
                return
            elif user_status.status == 'left':
                is_member = False
                if is_first_check:
                    await message.answer('Прошли уже сутки! Если Вы не вступите '
                                         'в течение следующих суток, Ваша анкета будет удалена',
                                         reply_markup=ReplyKeyboardRemove())
                    is_first_check = False
                    await asyncio.sleep(86_400)
                    break
                else:
                    await message.answer('Жаль, но придется нам расстаться. До свидания',
                                         reply_markup=ReplyKeyboardRemove())
                    await delete_user(user_id, channels)
                    await StartState.cycle.set()
                    return
        if is_member:
            await message.answer('Спасибо, что ты с нами!', reply_markup=ReplyKeyboardRemove())
            await state.finish()
            return


@dp.message_handler(state=StartState.get_moder)
async def get_moder(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == settings.SECRET_KEY:
        await update_user_status(message.from_user.id)
        await message.answer('Ваша анкета одобрена и права модератора получены',
                             reply_markup=CheckAccessKeyboard.get_reply_keyboard(add_stop=False))
        await state.finish()
    else:
        await message.answer('Неверный ключ доступа')
        await StartState.check_questionnaire.set()


@dp.message_handler(state=StartState.cycle)
async def cycle(message: types.Message):
    await StartState.cycle.set()


async def is_command(text: str) -> bool:
    if text.startswith('/'):
        return True
    return False
