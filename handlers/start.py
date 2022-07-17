from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from loader import dp
from keyboard.default.start_buttons import choice, agreement, gender, photo, universal_choice
from states.start_state import StartState
from aiogram.dispatcher.storage import FSMContext
from aiogram.types import ReplyKeyboardRemove


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = 'Приветствую! 👋 \nЭто телеграм бот "Школа IT". Чтобы продолжить наше общение, тебе нужно будет' \
           'прочесть наши правила и согласиться с ними :)'
    await message.answer(text, reply_markup=choice)
    await StartState.rules.set()


@dp.message_handler(state=StartState.rules)
async def reading_rules(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Ознакомиться с правилами 🤓':
        await message.answer('Тут говорится о правилах.', reply_markup=ReplyKeyboardRemove())
        await message.answer('Вы согласны с правилами?', reply_markup=agreement)
        await StartState.decision.set()
    elif answer == 'Я не буду читать правила 😐':
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
    if answer == 'Я согласен с правилами 😎':
        await message.answer('Хорошо, ваша заявка отправлена модератору и в скором времени будет рассмотрена 🔎',
                             reply_markup=ReplyKeyboardRemove())
        await message.answer('Супер! Модератор одобрил вашу заявку! Теперь займемся заполнением анкеты 📝')
        await message.answer('Введите ваше ФИО 🖊')
        await StartState.gender.set()
    elif answer == 'Я не согласен с правилами 🤔':
        await message.answer('Жаль, что вас не устроили наши правила 😔\nВ любой момент, если передумаете, можете'
                             'попробовать снова, для этого нажмите команду /start', reply_markup=ReplyKeyboardRemove())
        await state.reset_state()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision.set()


@dp.message_handler(state=StartState.gender)
async def get_user_gender(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(name=answer)
    await message.answer('Введите ваш пол', reply_markup=gender)
    await StartState.photo.set()


@dp.message_handler(state=StartState.photo)
async def ask_about_photo(message: types.Message, state: FSMContext):
    answer = message.text
    if answer == 'Мужской 👨':
        await state.update_data(gender='Мужской')
        await message.answer('Хотите ли вы загрузить свое фото?', reply_markup=photo)
        await StartState.decision_about_photo.set()
    elif answer == 'Женский 👩‍🦰':
        await state.update_data(gender='Женский')
        await message.answer('Хотите ли вы загрузить свое фото?', reply_markup=photo)
        await StartState.decision_about_photo.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.photo.set()


@dp.message_handler(state=StartState.decision_about_photo)
async def decision_about_photo(message: types.Message):
    answer = message.text
    if answer == 'Да! Хочу загрузить свою фоточку 😎':
        await message.answer('Супер!', reply_markup=ReplyKeyboardRemove())
        await StartState.upload_photo.set()
    elif answer == 'Нет, не буду загружать свое фото 🙂':
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
    await message.answer('Вы дизайнер? 🎨', reply_markup=universal_choice)
    await StartState.decision_about_design.set()


@dp.message_handler(state=StartState.decision_about_design)
async def decision_about_design(message: types.Message):
    answer = message.text
    if answer == 'Да ✅':
        await message.answer('Введите вашу ссылку на беханс 🌐', reply_markup=ReplyKeyboardRemove())
        await StartState.get_skills.set()
    elif answer == 'Нет ❌':
        await message.answer('Введите ваши навыки 💪', reply_markup=ReplyKeyboardRemove())
        await StartState.aims.set()
    else:
        await message.answer('Ошибка ввода! ⛔ \nВыберите один из предложенных вариантов')
        await StartState.decision_about_design.set()


@dp.message_handler(state=StartState.get_skills)
async def get_skills(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(behance=answer)
    await message.answer('Введите ваши навыки 💪')
    await StartState.aims.set()


@dp.message_handler(state=StartState.aims)
async def get_aims(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(skills=answer)
    await message.answer('Введите ваши цели 🎯')
    await StartState.finish_questions.set()


@dp.message_handler(state=StartState.finish_questions)
async def finish_questions(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(aims=answer)
    await message.answer('Ваша анкета отправлена на проверку. Пока ее не проверят функционал бота не доступен')
