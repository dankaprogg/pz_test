from pydantic import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    POSTGRES_DSN: str = Field(env='POSTGRES_DSN')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings_app = Settings()
