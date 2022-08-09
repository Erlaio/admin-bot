import asyncio
from typing import List

import aiosqlite
from pydantic import parse_obj_as

from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.department import Department


@connect_to_db
async def add_new_department(cur: aiosqlite.Cursor, department: str) -> None:
    await cur.execute('INSERT INTO departments (department) VALUES (?);', (department,))


@connect_to_db
async def attach_tl_to_department(cur: aiosqlite.Cursor, department: str, team_lead: str) -> None:
    await cur.execute('UPDATE departments SET (team_lead) = (?) WHERE department = ?',
                      (team_lead, department,))


@connect_to_db
async def get_department_by_id(cur: aiosqlite.Cursor, department_id: int) -> Department:
    await cur.execute(f'SELECT * FROM departments WHERE department_id = {department_id}')
    res = await cur.fetchone()
    data = parse_obj_as(Department, res)
    return data


@connect_to_db
async def get_all_departments(cur: aiosqlite.Cursor) -> List[Department]:
    await cur.execute(f'SELECT * FROM departments')
    records = await cur.fetchall()
    result = parse_obj_as(List[Department], records)
    return result


@connect_to_db
async def delete_department_by_id(cur: aiosqlite.Cursor, department_id: int) -> None:
    await cur.execute(f'DELETE FROM departments WHERE department_id={department_id}')


@connect_to_db
async def delete_department_by_name(cur: aiosqlite.Cursor, department_name: str) -> None:
    await cur.execute(f'DELETE FROM departments WHERE department = ?', (department_name,))


@connect_to_db
async def update_department_name(cur: aiosqlite.Cursor, old_name: str, new_name: str) -> None:
    await cur.execute(f'UPDATE departments SET (department) = (?) WHERE department = ?', (new_name, old_name))


@connect_to_db
async def update_department_by_id(cur: aiosqlite.Cursor, department_id: int, data: Department) -> None:
    await cur.execute(
        f'UPDATE departments SET (department, team_lead)=(?, ?) WHERE department_id={department_id}',
        (data.department, data.team_lead))


if __name__ == '__main__':
    # d = new_department(-1, "DepName1", "Leader1")
    # asyncio.run(add_new_department("NewDepName1"))
    # asyncio.run(attach_tl_to_department("NewDepName1", "NewLead1"))
    print(*asyncio.run(get_all_departments()), sep='\n')
    # print('', *get_all_departments(), sep='\n')
    # delete_department_by_id(11)
    # print(*get_all_departments(), sep='\n')
    # update_department_by_id(9, d)
    # print(*get_all_departments(), sep='\n')
