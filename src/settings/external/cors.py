"""
cors headers configuration, allows your resource
to be accessed on other domains
"""
from src.settings import base


base.INSTALLED_APPS.append("corsheaders")

base.MIDDLEWARE.extend([
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware"
])
