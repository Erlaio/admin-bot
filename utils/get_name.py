def split_fullname(fullname):
    try:
        surname = fullname.split()[0] if fullname.split()[0].isalpha() else ''
        name = fullname.split()[1] if fullname.split()[1].isalpha() else ''
        patronymic = fullname.split()[2] if fullname.split()[2].isalpha() else ''
    except IndexError:
        try:
            surname = fullname.split()[0] if fullname.split()[0].isalpha() else ''
            name = fullname.split()[1] if fullname.split()[1].isalpha() else ''
            patronymic = ''
        except IndexError:
            name = fullname if fullname.isalpha() else ''
            surname, patronymic = '', ''
    return surname, name, patronymic
