from environs import Env

from dataclasses import field
from dataclasses import dataclass


env = Env()
env.read_env()


@dataclass
class DatabaseSettings:
    DB_ENGINE: str = env.str("DB_ENGINE")
    DB_NAME: str = env.str("DB_NAME")
    DB_USER: str = env.str("DB_USER")
    DB_PASSWORD: str = env.str("DB_PASSWORD")
    DB_HOST: str = env.str("DB_HOST")
    DB_PORT: int = env.int("DB_PORT")
    DB_URL: str = env.str("DB_URL", "")

    def __post_init__(self):
        if not self.DB_URL:
            self.DB_URL = self.generate_db_url()

    def generate_db_url(self):
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


@dataclass
class CelerySettings:
    CELERY_BROKER_URL: str = env.str("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = env.str("CELERY_RESULT_BACKEND")
    CELERY_BEAT_SCHEDULER: str = env.str("CELERY_BEAT_SCHEDULER")
    CELERY_TIMEZONE: str = env.str("CELERY_TIMEZONE")
    CELERY_NOTIFY_INTERVAL: int = env.int("CELERY_NOTIFY_INTERVAL")


@dataclass
class DjangoSettings:
    DEBUG: bool = env.bool("DEBUG", False)
    SECRET_KEY: str = env.str("SECRET_KEY")
    ALLOWED_HOSTS: list[str] = field(default_factory=lambda: env.list("ALLOWED_HOSTS"))
    CSRF_TRUSTED_ORIGINS: list[str] = field(default_factory=lambda: env.list("CSRF_TRUSTED_ORIGINS"))


@dataclass
class SystemSettings:
    app: DjangoSettings = field(default_factory=DjangoSettings)
    db: DatabaseSettings = field(default_factory=DatabaseSettings)
    task: CelerySettings = field(default_factory=CelerySettings)


config = SystemSettings()
