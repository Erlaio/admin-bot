import asyncio
import random
from typing import List
import datetime

import aiosqlite
from pydantic import parse_obj_as

from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.user import User


@connect_to_db
async def add_new_user(cur: aiosqlite.Cursor, data: User) -> None:
    join_time = datetime.date.today()
    sql = '''INSERT INTO users (telegram_id, surname, name, patronymic, gender, 
    photo, email, git, behance, 
    tg_login, desired_department, 
    skills, goals, city, source_of_knowledge, lead_description, 
    join_time, is_moderator, is_approved) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?); '''
    await cur.execute(sql,
                      (data.telegram_id, data.surname, data.name, data.patronymic, data.gender, data.photo,
                       data.email, data.git, data.behance, data.tg_login, data.desired_department,
                       data.skills,
                       data.goals, data.city, data.source_of_knowledge,
                       data.lead_description, join_time, data.is_moderator,
                       data.is_approved))


@connect_to_db
async def get_user_by_id(cur: aiosqlite.Cursor, user_id: int) -> User:
    await cur.execute(f'SELECT * FROM users WHERE user_id = {user_id}')
    rec = await cur.fetchone()
    data = parse_obj_as(User, rec)
    return data


@connect_to_db
async def get_user_by_tg_login(cur: aiosqlite.Cursor, tg_login: str) -> User:
    await cur.execute(f'SELECT * FROM users WHERE tg_login = ?;', (tg_login,))
    rec = await cur.fetchone()
    data = parse_obj_as(User, rec)
    return data


@connect_to_db
async def get_user_by_tg_id(cur: aiosqlite.Cursor, tg_id: int) -> User or None:
    await cur.execute(f'SELECT * FROM users WHERE telegram_id = {tg_id};')
    rec = await cur.fetchone()
    if rec is None:
        return None
    data = parse_obj_as(User, rec)
    return data


@connect_to_db
async def get_all_users(cur: aiosqlite.Cursor) -> List[User]:
    await cur.execute(f'SELECT * FROM users')
    records = await cur.fetchall()
    result = parse_obj_as(List[User], records)
    return result


@connect_to_db
async def delete_user_by_id(cur: aiosqlite.Cursor, user_id: int) -> None:
    await cur.execute(f'DELETE FROM users WHERE user_id={user_id}')


@connect_to_db
async def delete_user_by_tg_id(cur: aiosqlite.Cursor, telegram_id: int) -> None:
    await cur.execute(f'DELETE FROM users WHERE telegram_id={telegram_id}')


@connect_to_db
async def update_user_status(cur: aiosqlite.Cursor, telegram_id: int) -> None:
    await cur.execute(f'UPDATE users SET is_moderator = (?), is_approved = (?) WHERE telegram_id = ?',
                      (1, 1, telegram_id))


@connect_to_db
async def update_user_by_id(cur: aiosqlite.Cursor, user_id: int, data: User) -> None:
    sql = '''UPDATE users SET (telegram_id, surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
    desired_department, skills, goals, city, source_of_knowledge, lead_description, join_time, is_moderator,
    is_approved) = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    await cur.execute(sql + f'WHERE user_id={user_id}',
                      (data.telegram_id, data.surname, data.name, data.patronymic, data.gender, data.photo,
                       data.email, data.git, data.behance, data.tg_login, data.desired_department,
                       data.skills, data.goals, data.city, data.source_of_knowledge,
                       data.lead_description, data.join_time, data.is_moderator,
                       data.is_approved))


@connect_to_db
async def update_user_by_telegram_id(cur: aiosqlite.Cursor, telegram_id: int, data: User) -> None:
    sql = '''UPDATE users SET (surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
    desired_department, skills, goals, city, source_of_knowledge, lead_description,
    join_time, is_moderator, is_approved) = (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    await cur.execute(sql + f'WHERE telegram_id={telegram_id}',
                      (data.surname, data.name, data.patronymic, data.gender, data.photo,
                       data.email, data.git, data.behance, data.tg_login, data.desired_department,
                       data.skills, data.goals, data.city, data.source_of_knowledge,
                       data.lead_description, data.join_time, data.is_moderator,
                       data.is_approved))


@connect_to_db
async def update_user_by_department(cur: aiosqlite.Cursor, user_id: int, data: User) -> None:
    sql = '''UPDATE users SET (telegram_id, surname, name, patronymic, gender, photo, email, git, behance, 
    tg_login, desired_department, skills, goals, city, source_of_knowledge, lead_description, join_time, 
    is_moderator,is_approved) = 
    (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    await cur.execute(sql + f'WHERE user_id={user_id}',
                      (data.telegram_id, data.surname, data.name, data.patronymic, data.gender, data.photo,
                       data.email, data.git, data.behance, data.tg_login, data.desired_department,
                       data.skills, data.goals, data.city, data.source_of_knowledge,
                       data.lead_description, data.join_time, data.is_moderator, data.is_approved))


@connect_to_db
async def update_lead_description(cur: aiosqlite.Cursor, telegram_id: int, description: str) -> None:
    await cur.execute('UPDATE users SET (lead_description) = (?)'
                      ' WHERE (telegram_id) = (?)', (description, telegram_id))


@connect_to_db
# useless for now
async def get_users_from_department(cur: aiosqlite.Cursor, department_id: int) -> List[User]:
    await cur.execute(f'SELECT * from users WHERE desired_department = {department_id};')
    records = await cur.fetchall()
    result = parse_obj_as(List[User], records)
    return result


@connect_to_db
async def get_users_from_department_name(cur: aiosqlite.Cursor, department_name: str) -> List[User]:
    await cur.execute(f'SELECT * from users WHERE desired_department = ?;', (department_name,))
    records = await cur.fetchall()
    result = parse_obj_as(List[User], records)
    return result


@connect_to_db
async def get_tg_id_if_moderator(cur: aiosqlite.Cursor) -> List[int]:
    await cur.execute(f'SELECT * from users WHERE is_moderator = 1;')
    records = await cur.fetchall()
    return [rec[1] for rec in records]


@connect_to_db
async def update_user_department(cur: aiosqlite.Cursor, old_name: str, new_name: str) -> None:
    await cur.execute('UPDATE users SET (desired_department) = (?) WHERE desired_department = ?',
                      (new_name, old_name))


@connect_to_db
async def get_unapproved_users(cur: aiosqlite.Cursor) -> List[User]:
    await cur.execute(f'SELECT * from users WHERE is_approved = ?', (0,))
    records = await cur.fetchall()
    result = parse_obj_as(List[User], records)
    return result


@connect_to_db
async def update_user_approve(cur: aiosqlite.Cursor, telegram_id: int) -> None:
    await cur.execute('UPDATE users SET (is_approved) = (?) WHERE telegram_id = ?', (1, telegram_id))


@connect_to_db
async def get_random_moder(cur: aiosqlite.Cursor) -> User:
    await cur.execute(f'SELECT * FROM users WHERE is_moderator = ?', (1,))
    records = await cur.fetchall()
    result = parse_obj_as(List[User], records)
    return random.choice(result)


@connect_to_db
async def update_field_value(cur: aiosqlite.Cursor, telegram_id: int, field: str, value) -> None:
    await cur.execute(f'UPDATE users SET {field} = (?) WHERE telegram_id = (?)', (value, telegram_id, ))


if __name__ == '__main__':
    # d = new_user(user_id=-1, behance='asdaljsdhjks', telegram_id=221152376508546261,
    # surname='gh', name='sldjkj', patronymic='asdfas', gender='', photo=bytearray(b''),
    # email='', git='', tg_login='', desired_department=-1, skills='', goals='', lead_description='',
    # join_time=datetime.date(2022, 7, 16), is_moderator=False, is_approved=False)
    # add_new_user(d)
    # print(get_user_by_id(10))
    # print(get_user_by_id(2))
    # print('', *get_all_users(), sep='\n')
    print(*asyncio.run(get_all_users()), sep='\n')
    # update_user_by_id(2, d)
    # print(get_user_by_id(3))
    # delete_user_by_id(3)
