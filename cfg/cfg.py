# -*- coding: utf-8 -*-
from envreader import EnvMissingError
from envreader import EnvReader
from envreader import EnvTransformError
from envreader import Field


class Config(EnvReader):
    # SQLITE_FILENAME: str = Field('blah.db', description="sqlite3 database file path")
    SECRET_KEY: str = Field(..., description="Admin Bot Secret Key")
    TELEGRAM_MODERS_CHAT_ID: int = Field(..., description="Moders_IDs")
    TELEGRAM_SCHOOL_CHATS: list = Field(..., description="School_Chat_ID")

    POSTGRES_HOSTNAME: str = Field(..., description='hostname')
    POSTGRES_DATABASE: str = Field(..., description='db_name')
    POSTGRES_USER: str = Field(..., description='user_name')
    POSTGRES_PASSWORD: str = Field(..., description='password')
    POSTGRES_PORT: int = Field(..., description='port_number')


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
