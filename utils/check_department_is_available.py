from pkg.db.department_func import get_all_departments


def is_department_available(message):
    department_name = message.text
    department_list = [i_elem.department for i_elem in get_all_departments()]
    return department_name in department_list
