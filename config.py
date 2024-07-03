from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):
    APP_ID: int
    APP_HASH: str
    PHONE_NUMBER: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
