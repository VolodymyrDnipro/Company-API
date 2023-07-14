from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')

    SERVER_PORT: int
    SERVER_HOST: str

    # database
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_ENDPOINT: str

    DATABASE_MAX_CONNECTIONS: int
    DATABASE_CONNECTION_RECYCLE: int

    # redis
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_URL: str


settings = Settings()