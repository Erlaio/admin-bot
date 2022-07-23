from pkg.db.department_func import get_all_departments
from pkg.db.project_func import get_all_projects


def is_department_available(name):
    department_list = [i_elem.department for i_elem in get_all_departments()]
    return name in department_list


def is_project_available(name):
    project_list = [i_elem.project_name for i_elem in get_all_projects()]
    return name in project_list
