import sqlite3
from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.department import Department, new_department
from typing import List


@connect_to_db
def add_new_department(cur: sqlite3.Cursor, data: Department):
    cur.execute("INSERT INTO departments (department, team_lead) VALUES (?, ?);", (data.department, data.team_lead))


@connect_to_db
def get_department_by_id(cur: sqlite3.Cursor, department_id: int) -> Department:
    cur.execute(f"SELECT * FROM departments WHERE department_id = {department_id}")
    res = cur.fetchone()
    data = new_department(res[0], res[1], res[2])
    return data


@connect_to_db
def get_all_departments(cur: sqlite3.Cursor) -> List[Department]:
    cur.execute(f"SELECT * FROM departments")
    records = cur.fetchall()
    result = []
    for record in records:
        data = new_department(record[0], record[1], record[2])
        result.append(data)
    return result


@connect_to_db
def delete_department_by_id(cur: sqlite3.Cursor, department_id: int):
    cur.execute(f"DELETE FROM departments WHERE department_id={department_id}")


@connect_to_db
def update_department_by_id(cur: sqlite3.Cursor, department_id: int, data: Department):
    cur.execute(f"UPDATE departments SET ( department, team_lead)=(?, ?) WHERE department_id={department_id}",
                (data.department, data.team_lead))


@connect_to_db
def get_users_from_department(cur: sqlite3.Cursor, department_id: int):
    cur.execute(f"SELECT * from users WHERE desired_department = {department_id};") # unsafe
    res = cur.fetchall()
    data = [field for field in res]
    return data


if __name__ == '__main__':
    d = new_department(-1, "DepName1", "Leader1")
    add_new_department(d)
    print(get_department_by_id(1))
    print('', *get_all_departments(), sep='\n')
    # delete_department_by_id(11)
    # print(*get_all_departments(), sep='\n')
    # update_department_by_id(9, d)
    # print(*get_all_departments(), sep='\n')
