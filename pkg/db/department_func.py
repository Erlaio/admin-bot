from typing import List

from pydantic import parse_obj_as

from pkg.db.db_connect import connect_to_db
from pkg.db.models.department import Department


async def add_new_department(department: str) -> None:
    async with connect_to_db() as conn:
        await conn.execute(
            'INSERT INTO departments (department) '
            'VALUES ($1);',
            department
        )


async def attach_tl_to_department(department: str, team_lead: str) -> None:
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


async def delete_department_by_id(department_id: int) -> None:
    async with connect_to_db() as conn:
        await conn.execute(
            'DELETE FROM departments '
            'WHERE department_id = $1;',
            department_id
        )


async def delete_department_by_name(department_name: str) -> None:
    async with connect_to_db() as conn:
        await conn.execute(
            'DELETE FROM departments '
            'WHERE department = $1;',
            department_name
        )


async def update_department_name(old_name: str, new_name: str) -> None:
    async with connect_to_db() as conn:
        await conn.execute(
            'UPDATE departments '
            'SET department = $1 '
            'WHERE department = $2;',
            new_name,
            old_name
        )


async def update_department_by_id(department_id: int, data: Department) -> None:
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
    # d = new_department(-1, "DepName1", "Leader1")
    # asyncio.run(add_new_department("NewDepName1"))
    # asyncio.run(attach_tl_to_department("NewDepName1", "NewLead1"))
    # print(*asyncio.run(get_all_departments()), sep='\n')
    # print('', *get_all_departments(), sep='\n')
    # delete_department_by_id(11)
    # print(*get_all_departments(), sep='\n')
    # update_department_by_id(9, d)
    # print(*get_all_departments(), sep='\n')
