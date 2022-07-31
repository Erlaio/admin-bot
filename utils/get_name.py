def get_fio(fio):
    try:
        surname = fio.split()[0] if fio.split()[0].isalpha() else ''
        name = fio.split()[1] if fio.split()[1].isalpha() else ''
        last_name = fio.split()[2] if fio.split()[2].isalpha() else ''
    except IndexError:
        try:
            surname = fio.split()[0] if fio.split()[0].isalpha() else ''
            name = fio.split()[1] if fio.split()[1].isalpha() else ''
            last_name = ''
        except IndexError:
            name = fio if fio.isalpha() else ''
            surname, last_name = '', ''
    return surname, name, last_name
