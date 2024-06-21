import os
from pathlib import Path
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-8h-aam*%&e+6c6^ws1_#h5*u$7k2@6+k6e7p2wgak#twqmm33l"

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'api',
    "drf_yasg",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "test_to_inforce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / 'templates']
        ,
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "test_to_inforce.wsgi.application"


USE_LOCAL_DB = os.getenv("USE_LOCAL_DB", True)

if USE_LOCAL_DB:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": os.getenv("SQL_ENGINE"),
            "NAME": os.getenv("SQL_NAME"),
            "USER": os.getenv("SQL_USER"),
            "PASSWORD": os.getenv("SQL_PASSWORD"),
            "HOST": os.getenv("SQL_HOST"),
            "PORT": os.getenv("SQL_PORT"),
        }
    }



AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = 'api.User'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    "EXCEPTION_HANDLER": "blast_courses.exceptions.core_exception_handler",
    "NON_FIELD_ERRORS_KEY": "error",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=50),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

DJOSER = {
    'LOGIN_FIELD': 'email',
    'USER_CREATE_PASSWORD_RETYPE': False,
    'SET_PASSWORD_RETYPE': False,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'USERNAME_CHANGED_EMAIL_CONFIRMATION': False,  # Вимкнути підтвердження електронної пошти
    'PASSWORD_CHANGED_EMAIL_CONFIRMATION': False,  # Вимкнути підтвердження електронної пошти
    'SEND_CONFIRMATION_EMAIL': False,  # Вимкнути надсилання підтвердження електронної пошти
    'SERIALIZERS': {
        'user_create': 'api.serializers.UserCreateSerializer',
        'user': 'api.serializers.UserSerializer',
        'current_user': 'api.serializers.UserSerializer',
        'user_delete': 'djoser.serializers.UserDeleteSerializer',
    },
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter JWT token as: Bearer <JWT>",
        }
    },
    "USE_SESSION_AUTH": False,
    "schemes": ["https"],
}
