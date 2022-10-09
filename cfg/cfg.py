# -*- coding: utf-8 -*-
import pydantic
from envreader import EnvMissingError
from envreader import EnvReader
from envreader import EnvTransformError
from envreader import Field


class Config(EnvReader):
    # SQLITE_FILENAME: str = Field('blah.db', description="sqlite3 database file path")
    SECRET_KEY: str = Field('asdf', description="Admin Bot Secret Key")
    TELEGRAM_MODERS_CHAT_ID: int = Field(-1001658648627, description="Moders_IDs")
    TELEGRAM_SCHOOL_CHATS: list = Field([-1001658648627, -1001770112839], description="School_Chat_ID")

    POSTGRES_HOSTNAME: str = Field('localhost', description='hostname')
    POSTGRES_DATABASE: str = Field('testdb', description='db_name')
    POSTGRES_USER: str = Field('postgres', description='user_name')
    POSTGRES_PASSWORD: str = Field('4er4er4er345', description='password')
    POSTGRES_PORT: int = Field('5432', description='port_number')


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
