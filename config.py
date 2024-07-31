from environs import Env

env = Env()
env.read_env()


class Config:
    DB_CONFIG = env(
        "DB_CONFIG",
        "postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}".format(
            DB_USER=env("DATABASE_USER"),
            DB_PASSWORD=env("DATABASE_PASS"),
            DB_HOST=env("DATABASE_HOST"),
            DB_NAME=env("DATABASE_NAME"),
        ),
    )
