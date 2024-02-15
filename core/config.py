from datetime import timedelta
from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    """
    Settings for JWT
    """
    private_key_path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_exp: timedelta = timedelta(days=1)


class Settings(BaseSettings):
    """
    Settings for app
    """

    DB_URL: str
    db_echo: bool = True
    auth_jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(env_file='.env', extra='allow')


settings = Settings()
