# HOST = '172.16.16.77'
HOST = '192.168.68.53'


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

    TABLE_USERS: str
    TABLE_TRIPS: str
    TABLE_TRIP_MEMBERS: str
    TABLE_LOCATION_HISTORY: str = "trip_location_history"

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int

    LINE_CHANNEL_ID: str
    LINE_CHANNEL_SECRET: str


settings = Settings()