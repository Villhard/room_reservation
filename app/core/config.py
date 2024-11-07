from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Бронирование переговорок"
    database_url: str
    secret: str = "secret"

    class Config:
        env_file = ".env"


settings = Settings()
