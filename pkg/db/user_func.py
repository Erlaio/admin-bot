import asyncio
import random

from typing import List

import aiosqlite

from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.user import User, new_user


@connect_to_db
async def add_new_user(cur: aiosqlite.Cursor, data: User):
    sql = '''INSERT INTO users (telegram_id, surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
                            desired_department, skills, goals, lead_description, join_time, is_moderator, is_approved)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    await cur.execute(sql,
                      (data.telegram_id, data.surname, data.name, data.patronymic, data.gender, data.photo,
                       data.email, data.git, data.behance, data.tg_login, data.desired_department,
                       data.skills,
                       data.goals, data.lead_description, data.join_time, data.is_moderator,
                       data.is_approved))


@connect_to_db
async def get_user_by_id(cur: aiosqlite.Cursor, user_id: int) -> User:
    await cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    rec = await cur.fetchone()
    data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                    gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                    tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                    lead_description=rec[14], join_time=rec[15], is_moderator=rec[16], is_approved=rec[17])
    return data


@connect_to_db
async def get_user_by_tg_login(cur: aiosqlite.Cursor, tg_login: str) -> User:
    await cur.execute(f"SELECT * FROM users WHERE tg_login = ?;", (tg_login,))
    rec = await cur.fetchone()
    data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                    gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                    tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                    lead_description=rec[14], join_time=rec[15], is_moderator=rec[16], is_approved=rec[17])
    return data


@connect_to_db
async def get_user_by_tg_id(cur: aiosqlite.Cursor, tg_id: int) -> User or None:
    await cur.execute(f"SELECT * FROM users WHERE telegram_id = {tg_id};")
    rec = await cur.fetchone()
    if rec is None:
        return None
    data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                    gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                    tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                    lead_description=rec[14], join_time=rec[15], is_moderator=rec[16], is_approved=rec[17])
    return data


@connect_to_db
async def get_all_users(cur: aiosqlite.Cursor) -> List[User]:
    await cur.execute(f"SELECT * FROM users")
    records = await cur.fetchall()
    result = []
    for rec in records:
        data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                        gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                        tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                        lead_description=rec[14], join_time=rec[15], is_moderator=rec[16],
                        is_approved=rec[17])
        result.append(data)
    return result


@connect_to_db
async def delete_user_by_id(cur: aiosqlite.Cursor, user_id: int):
    await cur.execute(f"DELETE FROM users WHERE user_id={user_id}")


@connect_to_db
async def delete_user_by_tg_id(cur: aiosqlite.Cursor, telegram_id: int):
    await cur.execute(f"DELETE FROM users WHERE telegram_id={telegram_id}")


@connect_to_db
async def update_user_status(cur: aiosqlite.Cursor, telegram_id: int):
    await cur.execute(f'UPDATE users SET is_moderator = (?), is_approved = (?) WHERE telegram_id = ?',
                      (1, 1, telegram_id))


@connect_to_db
async def update_user_by_id(cur: aiosqlite.Cursor, user_id: int, data: User):
    sql = '''UPDATE users SET (telegram_id, surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
                            desired_department, skills, goals, lead_description, join_time, is_moderator,is_approved)=
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    await cur.execute(sql + f"WHERE user_id={user_id}",
                      (data.telegram_id, data.surname, data.name, data.patronymic, data.gender, data.photo,
                       data.email, data.git, data.behance, data.tg_login, data.desired_department,
                       data.skills,
                       data.goals, data.lead_description, data.join_time, data.is_moderator,
                       data.is_approved))


@connect_to_db
async def update_user_by_telegram_id(cur: aiosqlite.Cursor, telegram_id: int, data: User):
    sql = '''UPDATE users SET (surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
                            desired_department, skills, goals, lead_description, join_time, is_moderator,is_approved)=
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    await cur.execute(sql + f"WHERE telegram_id={telegram_id}",
                      (data.surname, data.name, data.patronymic, data.gender, data.photo,
                       data.email, data.git, data.behance, data.tg_login, data.desired_department,
                       data.skills,
                       data.goals, data.lead_description, data.join_time, data.is_moderator,
                       data.is_approved))


@connect_to_db
async def update_user_by_department(cur: aiosqlite.Cursor, user_id: int, data: User):
    sql = '''UPDATE users SET (telegram_id, surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
                            desired_department, skills, goals, lead_description, join_time, is_moderator,is_approved)=
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    await cur.execute(sql + f"WHERE user_id={user_id}",
                      (data.telegram_id, data.surname, data.name, data.patronymic, data.gender, data.photo,
                       data.email, data.git, data.behance, data.tg_login, data.desired_department,
                       data.skills,
                       data.goals, data.lead_description, data.join_time, data.is_moderator,
                       data.is_approved))


@connect_to_db
async def get_users_from_department(cur: aiosqlite.Cursor, department_id: int):  # useless for now
    await cur.execute(f"SELECT * from users WHERE desired_department = {department_id};")
    records = await cur.fetchall()
    result = []
    for rec in records:
        data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                        gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                        tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                        lead_description=rec[14], join_time=rec[15], is_moderator=rec[16],
                        is_approved=rec[17])
        result.append(data)
    return result


@connect_to_db
async def get_users_from_department_name(cur: aiosqlite.Cursor, department_name: str):
    await cur.execute(f"SELECT * from users WHERE desired_department = ?;", (department_name,))
    records = await cur.fetchall()
    result = []
    for rec in records:
        data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                        gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                        tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                        lead_description=rec[14], join_time=rec[15], is_moderator=rec[16],
                        is_approved=rec[17])
        result.append(data)
    return result


@connect_to_db
async def get_tg_id_if_moderator(cur: aiosqlite.Cursor):
    await cur.execute(f"SELECT * from users WHERE is_moderator = 1;")
    records = await cur.fetchall()
    return [rec[1] for rec in records]


@connect_to_db
async def update_user_department(cur: aiosqlite.Cursor, old_name: str, new_name: str) -> None:
    await cur.execute("UPDATE users SET (desired_department) = (?) WHERE desired_department = ?",
                      (new_name, old_name))


@connect_to_db
async def get_unapproved_users(cur: aiosqlite.Cursor):
    await cur.execute(f"SELECT * from users WHERE is_approved = ?", (0,))
    records = await cur.fetchall()
    result = []
    for rec in records:
        data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                        gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                        tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                        lead_description=rec[14], join_time=rec[15])
        result.append(data)
    return result


@connect_to_db
async def update_user_approve(cur: aiosqlite.Cursor, telegram_id: int) -> None:
    await cur.execute("UPDATE users SET (is_approved) = (?) WHERE telegram_id = ?", (1, telegram_id))


@connect_to_db
async def get_random_moder(cur: aiosqlite.Cursor) -> User:
    await cur.execute(f"SELECT * FROM users WHERE is_moderator = ?", (1,))
    records = await cur.fetchall()
    result = []
    for rec in records:
        data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                        gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                        tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                        lead_description=rec[14], join_time=rec[15], is_moderator=rec[16],
                        is_approved=rec[17])
        result.append(data)
    return random.choice(result)


# @connect_to_db                                                                # useless for now
# def get_department_name(cur: sqlite3.Cursor, department_id: int):
#     cur.execute(f"SELECT department FROM departments WHERE department_id = {department_id}")
#     record = cur.fetchone()
#     return record[0]


if __name__ == '__main__':
    # d = new_user(user_id=-1, behance='asdaljsdhjks', telegram_id=221152376508546261, surname='gh', name='sldjkj', patronymic='asdfas', gender='', photo=bytearray(b''), email='', git='', tg_login='', desired_department=-1, skills='', goals='', lead_description='', join_time=datetime.date(2022, 7, 16), is_moderator=False, is_approved=False)
    # add_new_user(d)
    # print(get_user_by_id(10))
    # print(get_user_by_id(2))
    # print('', *get_all_users(), sep='\n')
    print(*asyncio.run(get_all_users()), sep='\n')
    # update_user_by_id(2, d)
    # print(get_user_by_id(3))
    # delete_user_by_id(3)
