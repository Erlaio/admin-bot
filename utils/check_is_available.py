from pkg.db.department_func import get_all_departments
from pkg.db.project_func import get_all_projects


async def is_department_available(name):
    departments = await get_all_departments
    department_list = [i_elem.department for i_elem in departments]
    return name in department_list


async def is_project_available(name):
    projects = await get_all_projects
    project_list = [i_elem.project_name for i_elem in projects]
    return name in project_list
