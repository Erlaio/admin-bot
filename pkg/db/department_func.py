from typing import List

from pydantic import parse_obj_as

from pkg.db.db_connect import connect_to_db
from pkg.db.models.department import Department


async def add_new_department(department: str):
    async with connect_to_db() as conn:
        await conn.execute(
            'INSERT INTO departments (department) '
            'VALUES ($1);',
            department
        )


async def attach_tl_to_department(department: str, team_lead: str):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE departments SET team_lead = $1 '
            'WHERE department = $2;',
            team_lead,
            department
        )


async def get_department_by_id(department_id: int) -> Department:
    async with connect_to_db() as conn:
        rec = await conn.fetchrow(
            'SELECT * FROM departments '
            'WHERE department_id = $1;',
            department_id
        )
    data = parse_obj_as(Department, rec)
    return data


async def get_all_departments() -> List[Department]:
    async with connect_to_db() as conn:
        rec = await conn.fetch(
            'SELECT * FROM departments;'
        )
    result = parse_obj_as(List[Department], rec)
    return result


async def delete_department_by_id(department_id: int):
    async with connect_to_db() as conn:
        await conn.execute(
            'DELETE FROM departments '
            'WHERE department_id = $1;',
            department_id
        )


async def delete_department_by_name(department_name: str):
    async with connect_to_db() as conn:
        await conn.execute(
            'DELETE FROM departments '
            'WHERE department = $1;',
            department_name
        )


async def update_department_name(old_name: str, new_name: str):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE departments '
            'SET department = $1 '
            'WHERE department = $2;',
            new_name,
            old_name
        )


async def update_department_by_id(department_id: int, data: Department):
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE departments '
            'SET department = $1, team_lead = $2 '
            'WHERE department_id = $3;',
            data.department,
            data.team_lead,
            department_id
        )


if __name__ == '__main__':
    pass
