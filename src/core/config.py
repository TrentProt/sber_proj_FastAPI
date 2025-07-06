from pathlib import Path

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR / 'certs' / 'jwt-private.pem'
    public_key_path: Path = BASE_DIR / 'certs' / 'jwt-public.pem'
    algorithm: str = 'RS256'
    access_token_expire_minutes: int = 60
    refresh_token_expire_minutes: int = 43200


class RunConfig(BaseModel):
    host: str = '0.0.0.0'
    port: int = 8000


class ApiPrefix(BaseModel):
    prefix: str = '/api/v1'


class DataBaseConfig(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='APP_CONFIG__',
        env_file='src/.env'
    )
    auth_jwt: AuthJWT = AuthJWT()
    api: ApiPrefix = ApiPrefix()
    run: RunConfig = RunConfig()
    db: DataBaseConfig


settings = Settings()

