import sqlite3
from pkg.settings import settings


def connect_to_db(func):
    def wrapper(*args, **kwargs):
        result = []
        try:
            conn = sqlite3.connect(r'../../'+settings.SQLITE_FILENAME)
            cur = conn.cursor()
            result = func(cur, *args, **kwargs)
        except sqlite3.Error as e:
            print("SQLite3 Error: ", e)
        finally:
            conn.commit()
            conn.close()
        return result
    return wrapper
