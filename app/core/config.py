import os


assert os.getenv("DB_USER") is not None, "DB_USER environment variable must be defined"

assert (
    os.getenv("DB_PASSWORD") is not None
), "DB_PASSWORD environment variable must be defined"

assert (
    os.getenv("DB_HOST") is not None
), "DB_HOST environment variable must be defined (e.g. : fastapi-postgresql)"

assert (
    os.getenv("DB_PORT") is not None
), "DB_HOST environment variable must be defined (e.g. : 5432)"

assert os.getenv("DB_NAME") is not None, "DB_NAME environment vairable must be defined"


class Config:
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    DB_CONFIG = os.getenv(
        "DB_CONFIG",
        f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    )


config = Config
