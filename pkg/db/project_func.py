import sqlite3
from typing import List

from pkg.db.db_connect_sqlite import connect_to_db
from pkg.db.models.project import Project, new_project


@connect_to_db
def add_new_project(cur: sqlite3.Cursor, project_name: str) -> None:
    cur.execute("INSERT INTO projects (project_name) VALUES (?);", (project_name,))


@connect_to_db
def attach_tl_to_project(cur: sqlite3.Cursor, project_name: str, team_lead: str) -> None:
    cur.execute("UPDATE projects SET (team_lead) = (?) WHERE project_name = ?", (team_lead, project_name,))


@connect_to_db
def get_all_projects(cur: sqlite3.Cursor) -> List[Project]:
    cur.execute("SELECT * FROM projects")
    records = cur.fetchall()
    result = []
    for record in records:
        data = new_project(record[0], record[1], record[2])
        result.append(data)
    return result


@connect_to_db
def delete_project_by_name(cur: sqlite3.Cursor, project_name: str) -> None:
    cur.execute(f"DELETE FROM projects WHERE project_name = ?", (project_name,))


@connect_to_db
def update_project_name(cur: sqlite3.Cursor, old_name: str, new_name: str) -> None:
    cur.execute(f"UPDATE projects SET (project_name) = (?) WHERE project_name = ?", (new_name, old_name))


if __name__ == '__main__':
    pass
    # add_new_project('TestProject')
