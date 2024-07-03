from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["settings"]


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
