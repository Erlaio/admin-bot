import pydantic
from cfg.cfg import config as cfg


class Settings():
    SQLITE_FILENAME: str = cfg.SQLITE_FILENAME
    SECRET_KEY: str = cfg.SECRET_KEY
    TELEGRAM_MODERS_CHAT_ID: int = cfg.TELEGRAM_MODERS_CHAT_ID
    TELEGRAM_SCHOOL_CHATS: list = cfg.TELEGRAM_SCHOOL_CHATS


def _get_settings() -> Settings:
    settings = Settings()
    return settings
