import aiosqlite
from typing import List
from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.project import Project, new_project


@connect_to_db
async def add_new_project(cur: aiosqlite.Cursor, project_name: str) -> None:
    await cur.execute('INSERT INTO projects (project_name) VALUES (?);', (project_name,))


@connect_to_db
async def attach_tl_to_project(cur: aiosqlite.Cursor, project_name: str, team_lead: str) -> None:
    await cur.execute('UPDATE projects SET (team_lead) = (?) WHERE project_name = ?', (team_lead, project_name,))


@connect_to_db
async def get_all_projects(cur: aiosqlite.Cursor) -> List[Project]:
    await cur.execute('SELECT * FROM projects')
    records = await cur.fetchall()
    result = []
    for record in records:
        data = new_project(record[0], record[1], record[2])
        result.append(data)
    return result


@connect_to_db
async def delete_project_by_name(cur: aiosqlite.Cursor, project_name: str) -> None:
    await cur.execute(f'DELETE FROM projects WHERE project_name = ?', (project_name,))


@connect_to_db
async def update_project_name(cur: aiosqlite.Cursor, old_name: str, new_name: str) -> None:
    await cur.execute(f'UPDATE projects SET (project_name) = (?) WHERE project_name = ?', (new_name, old_name))


if __name__ == '__main__':
    pass
    # asyncio.run(add_new_project('TestProject'))
