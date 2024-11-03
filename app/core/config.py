from pydantic import BaseSettings


class Settings(BaseSettings):
    app_title: str = "Бронирование переговорных комнат"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
