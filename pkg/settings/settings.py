from dotenv import find_dotenv
import pydantic


class _Settings(pydantic.BaseSettings):
    class Config:
        env_file_encoding = "utf-8"


class Settings(_Settings):
    SQLITE_FILENAME: str
    SECRET_KEY: str


def _get_settings() -> Settings:
    settings = Settings(_env_file=find_dotenv(".env"))
    return settings
