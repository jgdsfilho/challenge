from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    class ConfigDict:
        env_file = ".env"
        env_file_encoding = "utf-8"

    debug: bool = False
    db_async_connection_str: str
