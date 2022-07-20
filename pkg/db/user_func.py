import sqlite3
import datetime

from typing import List

from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.user import User, new_user


@connect_to_db
def add_new_user(cur: sqlite3.Cursor, data: User):
    sql = '''INSERT INTO users (telegram_id, surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
                            desired_department, skills, goals, lead_description, join_time, is_moderator, is_approved)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    cur.execute(sql, (data.telegram_id, data.surname, data.name, data.patronymic, data.gender, data.photo,
                      data.email, data.git, data.behance, data.tg_login, data.desired_department, data.skills,
                      data.goals, data.lead_description, data.join_time, data.is_moderator, data.is_approved))


@connect_to_db
def get_user_by_id(cur: sqlite3.Cursor, user_id: int) -> User:
    cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    rec = cur.fetchone()
    data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                    gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                    tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                    lead_description=rec[14], join_time=rec[15], is_moderator=rec[16], is_approved=rec[17])
    return data


@connect_to_db
def get_user_by_tg_login(cur: sqlite3.Cursor, tg_login: str) -> User:
    cur.execute(f"SELECT * FROM users WHERE tg_login = ?;", (tg_login, ))
    rec = cur.fetchone()
    data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                    gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                    tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                    lead_description=rec[14], join_time=rec[15], is_moderator=rec[16], is_approved=rec[17])
    return data


@connect_to_db
def get_all_users(cur: sqlite3.Cursor) -> List[User]:
    cur.execute(f"SELECT * FROM users")
    records = cur.fetchall()
    result = []
    for rec in records:
        data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                        gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                        tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                        lead_description=rec[14], join_time=rec[15], is_moderator=rec[16], is_approved=rec[17])
        result.append(data)
    return result


@connect_to_db
def delete_user_by_id(cur: sqlite3.Cursor, user_id: int):
    cur.execute(f"DELETE FROM users WHERE user_id={user_id}")


@connect_to_db
def update_user_by_id(cur: sqlite3.Cursor, user_id: int, data: User):
    sql = '''UPDATE users SET (telegram_id, surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
                            desired_department, skills, goals, lead_description, join_time, is_moderator,is_approved)=
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur.execute(sql + f"WHERE user_id={user_id}",
                (data.telegram_id, data.surname, data.name, data.patronymic, data.gender, data.photo,
                 data.email, data.git, data.behance, data.tg_login, data.desired_department, data.skills,
                 data.goals, data.lead_description, data.join_time, data.is_moderator, data.is_approved))


@connect_to_db
def update_user_by_telegram_id(cur: sqlite3.Cursor, telegram_id: int, data: User):
    sql = '''UPDATE users SET (surname, name, patronymic, gender, photo, email, git, behance, tg_login, 
                            desired_department, skills, goals, lead_description, join_time, is_moderator,is_approved)=
                            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur.execute(sql + f"WHERE telegram_id={telegram_id}",
                (data.surname, data.name, data.patronymic, data.gender, data.photo,
                 data.email, data.git, data.behance, data.tg_login, data.desired_department, data.skills,
                 data.goals, data.lead_description, data.join_time, data.is_moderator, data.is_approved))


@connect_to_db
def get_users_from_department(cur: sqlite3.Cursor, department_id: int):
    cur.execute(f"SELECT * from users WHERE desired_department = {department_id};") # unsafe
    records = cur.fetchall()
    result = []
    for rec in records:
        data = new_user(user_id=rec[0], telegram_id=rec[1], surname=rec[2], name=rec[3], patronymic=rec[4],
                        gender=rec[5], photo=rec[6], email=rec[7], git=rec[8], behance=rec[9],
                        tg_login=rec[10], desired_department=rec[11], skills=rec[12], goals=rec[13],
                        lead_description=rec[14], join_time=rec[15], is_moderator=rec[16], is_approved=rec[17])
        result.append(data)
    return result


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
    print('', *get_all_users(), sep='\n')
    # update_user_by_id(2, d)
    # print(get_user_by_id(3))
    # delete_user_by_id(3)
