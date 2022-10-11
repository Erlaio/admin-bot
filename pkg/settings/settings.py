import pydantic
from dotenv import find_dotenv


class _Settings(pydantic.BaseSettings):
    class Config:
        env_file_encoding = "utf-8"


class Settings(_Settings):
    # PostgresQL
    #BOT_KEY: pydantic.SecretStr
    POSTGRES_HOSTNAME: str
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int

    # BaseSettings
    # SQLITE_FILENAME: str = cfg.SQLITE_FILENAME
    SECRET_KEY: str
    TELEGRAM_MODERS_CHAT_ID: int
    TELEGRAM_SCHOOL_CHATS: list


def _get_settings() -> Settings:
    settings = Settings(_env_file=find_dotenv('.env'))
    return settings
