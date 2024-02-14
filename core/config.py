from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class Settings(BaseSettings):
    """
    Settings for app
    """

    DB_URL: str
    model_config = SettingsConfigDict(env_file='.env', extra='allow')


settings = Settings()
