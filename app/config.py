from environs import Env

env = Env()
env.read_env()


class Config:

    DMS_NAME: str = env.str("DMS_NAME")
    DB_USER: str = env.str("POSTGRES_USER")
    DB_PASSWORD: str = env.str("POSTGRES_PASSWORD")
    DB_NAME: str = env.str("POSTGRES_DB")
    DB_HOST: str = env.str("DB_HOST")
    DB_DRIVER: str = env.str("DB_DRIVER")

    DATABASE_URL = f"{DMS_NAME}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    ALEMBIC_DATABASE_URL = f"{DMS_NAME}+{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@185.247.185.176:5432/{DB_NAME}"
