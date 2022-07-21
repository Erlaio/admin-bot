def is_available(name, func):
    department_list = [i_elem.department for i_elem in func()]
    return name in department_list
