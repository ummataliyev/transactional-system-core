import dj_database_url

from src.settings.config.config import config


DATABASES = {
    'default': dj_database_url.config(default=config.DB_URL)
}
