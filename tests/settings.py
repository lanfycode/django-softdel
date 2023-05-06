import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-secure-key'
DEBUG = True
INSTALLED_APPS = [
    "softdel",
    "tests",
]

MIDDLEWARE = []
ROOT_URLCONF = "tests.urls"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': 'db_test'
        },
    }
}

USE_TZ = False
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SOFT_DELETE_FILTER_DELETED = True
SOFT_DELETE_COLLECT_RELATED = True
