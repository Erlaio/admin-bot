import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: int = 0
    telegram_id: int = ''
    surname: str = ''
    name: str = ''
    patronymic: str = ''
    gender: str = ''
    photo: bytearray = bytearray([])
    email: EmailStr = ''
    git: str = ''
    behance: str = ''
    tg_login: str = ''
    desired_department: int = -1
    skills: str = ''
    goals: str = ''
    lead_description: str = ''
    join_time: datetime.date = datetime.date(day=1, month=1, year=1)
    is_moderator: bool = False
    is_approved: bool = False

    class Config:
        arbitrary_types_allowed = True


def new_user(user_id=-1, telegram_id=-1, surname='', name='', patronymic='', gender='', photo=bytearray([]), email='',
             git='', behance='', tg_login='', desired_department=-1, skills='', goals='', lead_description='',
             join_time=None, is_moderator=False, is_approved=False):
    if join_time is None:
        join_time = datetime.date.today()

    res = User()
    res.user_id = user_id
    res.telegram_id = telegram_id
    res.surname = surname
    res.name = name
    res.patronymic = patronymic
    res.gender = gender
    res.photo = photo
    res.email = email
    res.git = git
    res.behance = behance
    res.tg_login = tg_login
    res.desired_department = desired_department
    res.skills = skills
    res.goals = goals
    res.lead_description = lead_description
    res.join_time = join_time
    res.is_moderator = is_moderator
    res.is_approved = is_approved
    return res
