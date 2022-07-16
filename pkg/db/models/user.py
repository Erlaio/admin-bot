import datetime
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    user_id: int = 0
    surname: str = ''
    name: str = ''
    patronymic: str = ''
    gender: str = ''
    photo: bytearray = bytearray([])
    email: EmailStr = ''
    git: str = ''
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


def new_user(user_id=-1, surname='', name='', patronymic='', gender='', photo=bytearray([]), email='',
                   git='', tg_login='', desired_department=-1, skills='', goals='', lead_description='',
                   join_time='0001-01-01', is_moderator=False, is_approved=False):
    res = User()
    res.user_id = user_id
    res.surname = surname
    res.name = name
    res.patronymic = patronymic
    res.gender = gender
    res.photo = photo
    res.email = email
    res.git = git
    res.tg_login = tg_login
    res.desired_department = desired_department
    res.skills = skills
    res.goals = goals
    res.lead_description = lead_description
    res.join_time = join_time
    res.is_moderator = is_moderator
    res.is_approved = is_approved
    return res
