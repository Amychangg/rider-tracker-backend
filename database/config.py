from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    DB_MIN_CONN: int = 1
    DB_MAX_CONN: int = 10


settings = Settings()


TABLE_USERS = 'users'
TABLE_TRIPS = 'trips'
TABLE_TRIP_MEMBERS = 'trip_members'

