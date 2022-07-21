import sqlite3
from typing import List

from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.department import Department, new_department


@connect_to_db
def add_new_department(cur: sqlite3.Cursor, department: str) -> None:
    cur.execute("INSERT INTO departments (department) VALUES (?);", (department,))


@connect_to_db
def attach_tl_to_department(cur: sqlite3.Cursor, department: str, team_lead: str) -> None:
    cur.execute("UPDATE departments SET (team_lead) = (?) WHERE department = ?", (team_lead, department,))


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
def delete_department_by_id(cur: sqlite3.Cursor, department_id: int) -> None:
    cur.execute(f"DELETE FROM departments WHERE department_id={department_id}")


@connect_to_db
def delete_department_by_name(cur: sqlite3.Cursor, department_name: str) -> None:
    cur.execute(f"DELETE FROM departments WHERE department = ?", (department_name,))


@connect_to_db
def update_department_name(cur: sqlite3.Cursor, old_name: str, new_name: str) -> None:
    cur.execute(f"UPDATE departments SET (department) = (?) WHERE department = ?", (new_name, old_name))


@connect_to_db
def update_department_by_id(cur: sqlite3.Cursor, department_id: int, data: Department) -> None:
    cur.execute(f"UPDATE departments SET (department, team_lead)=(?, ?) WHERE department_id={department_id}",
                (data.department, data.team_lead))


if __name__ == '__main__':
    d = new_department(-1, "DepName1", "Leader1")
    add_new_department(d)
    print(get_department_by_id(1))
    print('', *get_all_departments(), sep='\n')
    # delete_department_by_id(11)
    # print(*get_all_departments(), sep='\n')
    # update_department_by_id(9, d)
    # print(*get_all_departments(), sep='\n')
