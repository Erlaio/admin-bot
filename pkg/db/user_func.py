import sqlite3
import datetime
import time

from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.user import User, new_user


@connect_to_db
def add_new_user(cur: sqlite3.Cursor, data: User):
    sql = '''INSERT INTO users (surname, name, patronymic, gender, photo, email, git, tg_login, desired_department, 
                                skills, goals, lead_description, join_time, is_moderator,is_approved)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'''
    cur.execute(sql, (data.surname, data.name, data.patronymic, data.gender, data.photo,
                      data.email, data.git, data.tg_login, data.desired_department, data.skills,
                      data.goals, data.lead_description, data.join_time, data.is_moderator, data.is_approved))


@connect_to_db
def get_user_by_id(cur: sqlite3.Cursor, user_id: int) -> User:
    cur.execute(f"SELECT * FROM users WHERE user_id = {user_id}")
    rec = cur.fetchone()
    data = new_user(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9], rec[10],
                    rec[11], rec[12], rec[13], rec[14], rec[15])
    return data


@connect_to_db
def get_all_users(cur: sqlite3.Cursor) -> list[User]:
    cur.execute(f"SELECT * FROM users")
    records = cur.fetchall()
    result = []
    for rec in records:
        data = new_user(rec[0], rec[1], rec[2], rec[3], rec[4], rec[5], rec[6], rec[7], rec[8], rec[9], rec[10],
                        rec[11], rec[12], rec[13], rec[14], rec[15])
        result.append(data)
    return result


@connect_to_db
def delete_user_by_id(cur: sqlite3.Cursor, user_id: int):
    cur.execute(f"DELETE FROM users WHERE user_id={user_id}")


@connect_to_db
def update_user_by_id(cur: sqlite3.Cursor, user_id: int, data: User):
    sql = '''UPDATE users SET (surname, name, patronymic, gender, photo, email, git, tg_login, desired_department, 
                                skills, goals, lead_description, join_time, is_moderator,is_approved)=
                                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) '''
    cur.execute(sql + f"WHERE user_id={user_id}",
                (data.surname, data.name, data.patronymic, data.gender, data.photo,
                data.email, data.git, data.tg_login, data.desired_department, data.skills,
                data.goals, data.lead_description, data.join_time, data.is_moderator, data.is_approved))


if __name__ == '__main__':
    d = new_user(-1, "surname", "name", "patronymic", "m", b'', "mail@mail.ru", r"http://git.com",
                 "@TG", 0, "My Skills", "My Goals", "Lead Desc", datetime.date.today(), False, False)
    add_new_user(d)
    print(get_user_by_id(1))
    print('', *get_all_users(), sep='\n')
    # delete_user_by_id(2)
    # print('', *get_all_users(), sep='\n')
    # update_user_by_id(2, d)
    # print(get_user_by_id(2))
