from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    db_url: str = 'postgresql+asyncpg://test:test@localhost/sber'
    db_echo: bool = True

settings = Settings()

