"""
swagger configuration
"""
from src.settings import base

base.INSTALLED_APPS.extend([
    "drf_yasg",
])


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token-based authentication. Format: "Token <your-token>"'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
    'SUPPORTED_SUBMIT_METHODS': ['get', 'post', 'put', 'delete', 'patch'],
}

REDOC_SETTINGS = {
    'LAZY_RENDERING': False,
}
