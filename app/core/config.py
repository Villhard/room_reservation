from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Бронирование переговорных комнат"

    class Config:
        env_file = ".env"


settings = Settings()
