# -*- coding: utf-8 -*-

from envreader import EnvReader
from envreader import Field
from envreader import EnvTransformError
from envreader import EnvMissingError

class Config(EnvReader):
    SQLITE_FILENAME: str = Field(..., description = "sqlite3 database file path")
    SECRET_KEY: str = Field(..., description = "Admin Bot Secret Key")
    TELEGRAM_MODERS_CHAT_ID: int = Field(..., description = "Moders_IDs")
    TELEGRAM_SCHOOL_CHATS: list = Field(..., description = "School_Chat_ID")

try:
    config = Config()

except EnvTransformError as e:
    print('Malformed environment parameter {}!'.format(e.field))
    print('Settings help:\n' + Config(populate=False).help())
    print('Committing suicide...')

except EnvMissingError as e:
    print('Configuration key {} was not found in env!'.format(e.args[0]))
    print('Settings help:\n' + Config(populate=False).help())
    print('Committing suicide...')

