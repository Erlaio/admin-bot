import imghdr
import os.path
import time

import validators
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


async def is_command(text: str) -> bool:
    if text.startswith('/'):
        return True
    return False


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = 'Привет! ' \
           'Рады приветствовать Вас в Школе IT! ' \
           '\nШкола IT Terra создана для помощи благотворительным фондам и людям.' \
           ' Каждый участник вносит вклад в общее дело. ' \
           'Школа – это комьюнити, которое помогает прокачивать навыки всем желающим. Мы учимся новому и всегда ' \
           'готовы помочь каждому участнику разобраться с возникшим вопросом.  ' \
           '\nЗдесь собрались самые любознательные, целеустремленные и приветливые люди.' \
           ' Мы объединяем новичков и специалистов разных возрастов не только из разных городов России, но и мира. ' \
           '\nДля того чтобы попасть в Школу, просим ответить на несколько вопросов'
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
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, выберите один из предложенных вариантов ответа',
                             reply_markup=ChoiceKeyboard.get_reply_keyboard())
    elif answer == ChoiceKeyboard.B_READ_RULES:
        await message.answer(RULES, reply_markup=ReplyKeyboardRemove())
        await message.answer('Вы согласны с правилами?', reply_markup=AgreementKeyboard.get_reply_keyboard())
        await StartState.decision.set()
    elif answer == ChoiceKeyboard.A_DONT_READ_RULES:
        await message.answer(
            'Очень жаль, что наше с Вами общение подходит к концу 😔\nЕсли Вы передумаете, '
            'то я всегда тут! Нужно лишь повторно вызвать команду /start',
            reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.rules.set()


@dp.message_handler(state=StartState.decision)
async def decision_about_rules(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, выберите один из предложенных вариантов ответа',
                             reply_markup=AgreementKeyboard.get_reply_keyboard())
    elif answer == AgreementKeyboard.B_AGREE_WITH_RULES:
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
                             'В любой момент, если передумаете, можете '
                             'попробовать снова, для этого нажмите команду /start',
                             reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision.set()


@dp.message_handler(state=StartState.update_info)
async def update_info(message: types.Message):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, выберите один из предложенных вариантов ответа',
                             reply_markup=YesNoKeyboard.get_reply_keyboard())
    elif answer == YesNoKeyboard.B_YES:
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
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, выберите один из предложенных вариантов ответа',
                             reply_markup=YesNoKeyboard.get_reply_keyboard())
    elif answer == YesNoKeyboard.B_YES:
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
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите ваше ФИО',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    else:
        if len(answer.split(' ')) < 2:
            await message.answer('Пожалуйста, введите хотя бы фамилию и имя',
                                 reply_markup=StopBotKeyboard.get_reply_keyboard())
        else:
            surname, name, patronymic = split_fullname(answer)
            if name.isalpha():
                user = User()
                user.join_time = datetime.date.today()
                user.telegram_id = message.from_user.id
                user.tg_login = f'@{message.from_user.username}'
                user.surname, user.name, user.patronymic = surname, name, patronymic
                await add_new_user(user)
                await ContextHelper.add_user(user, state)
                await message.answer('Выберите Ваш пол',
                                     reply_markup=GenderKeyboard.get_reply_keyboard())
                await StartState.photo.set()
            else:
                await message.answer('Необходимо ввести ФИО\nПример: Иванов Иван Иванович\n'
                                     'Можно не указывать фамилию или отчество\nИмя указывать обязательно.')
                await StartState.gender.set()


@dp.message_handler(state=StartState.photo)
async def ask_about_photo(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, выберите один из предложенных вариантов ответа',
                             reply_markup=GenderKeyboard.get_reply_keyboard())
    else:
        message_text = 'Хотите ли Вы загрузить свое фото?'
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
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, выберите один из предложенных вариантов ответа',
                             reply_markup=PhotoKeyboard.get_reply_keyboard())
    else:
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
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите вашу почту',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    elif validators.email(answer):
        user = await ContextHelper.get_user(state)
        user.email = answer
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Выберите, в какой бы отдел Вы хотели попасть?',
                             reply_markup=await DepartmentsKeyboard.get_reply_keyboard())
        await StartState.department.set()
    else:
        await message.answer('Вы ввели неверный формат почты',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())


@dp.message_handler(state=StartState.department)
async def get_department(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите или выберите желаемый отдел',
                             reply_markup=await DepartmentsKeyboard.get_reply_keyboard())
    elif answer == 'Design':
        user = await ContextHelper.get_user(state)
        user.desired_department = answer
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите вашу ссылку на беханс 🌐',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.get_skills_design.set()
    else:
        user = await ContextHelper.get_user(state)
        user.desired_department = answer
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите вашу ссылку на gitlab 🌐',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.get_skills_dev.set()


@dp.message_handler(state=StartState.get_skills_design)
async def get_skills_design(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите ссылку на ваш Behance',
                             reply_markup=ReplyKeyboardRemove())
    elif not validators.url(answer):
        await message.answer('Введите, пожалуйста, корректную ссылку на Behance',
                             reply_markup=ReplyKeyboardRemove())
    else:
        user = await ContextHelper.get_user(state)
        user.behance = answer
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите, пожалуйста, из какого вы города',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.get_city.set()


@dp.message_handler(state=StartState.get_skills_dev)
async def get_skills_dev(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите ссылку на ваш Gitlab',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    elif not validators.url(answer):
        await message.answer('Введите, пожалуйста, корректную ссылку на Gitlab',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    else:
        user = await ContextHelper.get_user(state)
        user.git = answer
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите, пожалуйста, из какого вы города',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.get_city.set()


@dp.message_handler(state=StartState.get_city)
async def get_city(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите город, в котором проживаете',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    else:
        user = await ContextHelper.get_user(state)
        user.city = answer
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Напишите, пожалуйста, откуда Вы узнали о Школе IT?',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.get_source.set()


@dp.message_handler(state=StartState.get_source)
async def get_source(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите откуда Вы узнали о школе',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    else:
        user = await ContextHelper.get_user(state)
        user.source_of_knowledge = answer
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите ваши навыки\n'
                             'Например: Python, Postgresql, Git, FastAPI, '
                             'Django, Go, aiogramm, asyncio', reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.exceptations.set()


@dp.message_handler(state=StartState.exceptations)
async def get_goals(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите ваши навыки',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
    else:
        user = await ContextHelper.get_user(state)
        user.skills = answer
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите ваши основные ожидания от школы',
                             reply_markup=StopBotKeyboard.get_reply_keyboard())
        await StartState.development_vector.set()


@dp.message_handler(state=StartState.development_vector)
async def get_development_vector(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите ваши ожидания от школы',
                             reply_markup=StopBotKeyboard.get_reply_keyboard(add_stop=False))
    else:
        user = await ContextHelper.get_user(state)
        user.goals = f'Ожидания: {answer}'
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Введите желаемый вектор развития',
                             reply_markup=ReplyKeyboardRemove())
        await StartState.finish_questions.set()


@dp.message_handler(state=StartState.finish_questions)
async def finish_questions(message: types.Message, state: FSMContext):
    answer = message.text
    if await is_command(answer):
        await message.answer('Вы ввели команду. Пожалуйста, введите желаемый вектор развития',
                             reply_markup=StopBotKeyboard.get_reply_keyboard(add_stop=False))
    else:
        user = await ContextHelper.get_user(state)
        user.goals += f'\nВектор развития: {answer}'
        await update_user_by_telegram_id(message.from_user.id, user)
        await ContextHelper.add_user(user, state)
        await message.answer('Ваша анкета отправлена на проверку. '
                             'Пока ее не проверят, функционал бота не доступен',
                             reply_markup=CheckAccessKeyboard.get_reply_keyboard(add_stop=False))
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
    answer = message.text
    if answer == CheckAccessKeyboard.A_CHECK_ACCESS:
        try:
            user = await get_user_by_tg_login(f'@{message.from_user.username}')
            if user.is_approved:
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
            channels = settings.TELEGRAM_SCHOOL_CHATS
            user_id = message.from_user.id
            user_status = await bot.get_chat_member(chat_id=channels[0], user_id=user_id)

            if user_status.status == 'kicked':
                await bot.send_message(text='Вы заблокированы в одном из наших чатов. '
                                            'Обратитесь к тимлиду или модератору',
                                       chat_id=message.chat.id,
                                       reply_markup=ReplyKeyboardRemove())
                await StartState.cycle.set()
            else:
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
                    await message.answer('Если Вы не вступите '
                                         'в течение следующих суток, Ваша анкета будет удалена',
                                         reply_markup=ReplyKeyboardRemove())
                    is_first_check = False
                    await asyncio.sleep(86_400)
                    break
                else:
                    await bot.send_message(chat_id=settings.TELEGRAM_MODERS_CHAT_ID,
                                           text=f'Пользователь @{message.from_user.username} кикнут'
                                                f' по истечению двух суток')
                    await message.answer('Жаль, но придется нам расстаться. До свидания',
                                         reply_markup=ReplyKeyboardRemove())
                    await delete_user(user_id, channels)
                    await StartState.cycle.set()
                    return
        if is_member:
            await message.answer('Спасибо, что Вы с нами!', reply_markup=ReplyKeyboardRemove())
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
