from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp
from keyboard.default.button_value import ButtonValue as button
from keyboard.default.keyboard import Keyboard
from states.start_state import StartState


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
async def get_user_gender(message:types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer('Введите ваш пол', reply_markup=Keyboard.GENDER)
    await StartState.photo.set()


@dp.message_handler(state=StartState.photo)
async def ask_about_photo(message: types.Message, state: FSMContext):
    answer = message.text
    message_text = 'Хотите ли вы загрузить свое фото?'
    reply_markup = Keyboard.PHOTO
    if answer == button.MALE_GENDER:
        await state.update_data(gender='Мужской')
        await message.answer(message_text, reply_markup=reply_markup)
        await StartState.decision_about_photo.set()
    elif answer == button.FEMALE_GENDER:
        await state.update_data(gender='Женский')
        await message.answer(message_text, reply_markup=reply_markup)
        await StartState.decision_about_photo.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.photo.set()


@dp.message_handler(state=StartState.decision_about_photo)
async def decision_about_photo(message: types.Message):
    answer = message.text
    if answer == button.WANT_UPLOAD_PHOTO:
        await message.answer('Супер!', reply_markup=ReplyKeyboardRemove())
        await StartState.upload_photo.set()
    elif answer == button.DONT_WANT_UPLOAD_PHOTO:
        await message.answer('Хорошо, тогда продолжаем анкетирование 📝', reply_markup=ReplyKeyboardRemove())
        await message.answer('Введите вашу почту 📧')
        await StartState.gitlab.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision_about_photo.set()


@dp.message_handler(state=StartState.upload_photo)
async def upload_photo(message: types.Message):
    pass


@dp.message_handler(state=StartState.gitlab)
async def get_gitlab(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(email=answer)
    await message.answer('Введите вашу ссылку на gitlab 🌐')
    await StartState.design.set()


@dp.message_handler(state=StartState.design)
async def design(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(gitlab=answer)
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
        await StartState.aims.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision_about_design.set()


@dp.message_handler(state=StartState.get_skills)
async def get_skills(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(behance=answer)
    await message.answer('Введите ваши навыки\nТут нужно будет добавить шаблон')
    await StartState.aims.set()


@dp.message_handler(state=StartState.aims)
async def get_aims(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(skills=answer)
    await message.answer('Введите ваши цели\nТут нужно будет добавить шаблон')
    await StartState.finish_questions.set()


@dp.message_handler(state=StartState.finish_questions)
async def finish_questions(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(aims=answer)
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
        await StartState.check_questionnaire.set()
