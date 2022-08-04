import pathlib
from pkg.settings import settings
from utils.config_utils import ConfigUtils
import aiosqlite


def connect_to_db(func):
    async def wrapper(*args, **kwargs):
        result = []
        try:
            conn = await aiosqlite.connect(str(pathlib.PurePath(ConfigUtils.get_project_root(), settings.SQLITE_FILENAME)))
            cur = await conn.cursor()
            result = await func(cur, *args, **kwargs)
        except aiosqlite.Error as e:
            print('aiosqlite Error: ', e)
        finally:
            await conn.commit()
            await conn.close()
        return result
    return wrapper
