# from handlers.show_user_card_from_bd import get_all_users

class ButtonValue:
    READ_RULES = 'Ознакомиться с правилами 🤓'
    DONT_READ_RULES = 'Я не буду читать правила 😐'
    AGREE_WITH_RULES = 'Я согласен с правилами 😎'
    DONT_AGREE_WITH_RULES = 'Я не согласен с правилами 🤔'
    MALE_GENDER = 'Мужской 👨'
    FEMALE_GENDER = 'Женский 👩‍🦰'
    WANT_UPLOAD_PHOTO = 'Да! Хочу загрузить свою фоточку 😎'
    DONT_WANT_UPLOAD_PHOTO = 'Нет, не буду загружать свое фото 🙂'
    YES = 'Да ✅'
    NO = 'Нет ❌'
    CHECK_ACCESS = 'Проверить состояние анкеты ✅'

    VIEW_ALL = 'Посмотреть всех'
    VIEW_ID = 'Посмотреть по ID'
    VIEW_TG_LOGIN = 'Посмотреть по Логину в Telegram'

    FRONTEND = 'Frontend'
    BACKEND = 'Backend'
    ML = 'ML'
    DS = 'DS'
    DESIGN = 'Design'
    MOBILE_DEVELOPMENT = 'Mobile Development'

    # PAGES = [page for page in range(len(get_all_users()) // 2)]
    PAGES = [page for page in range(65)]
