"""
django rest-framework configuration
"""
from src.settings import base

base.INSTALLED_APPS.extend([
    "rest_framework",
])
