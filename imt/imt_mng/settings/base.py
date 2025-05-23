import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta

load_dotenv()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# get envs from file .env
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG", default=True)             
DEBUG = True           
ENVIRONMENT = os.getenv("DJANGO_ENV", default="local")
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "127.0.0.1").split(",")


# Application definition
DJANGO_CORE_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "phonenumber_field",
    "rest_framework",
    "drf_spectacular",
    "corsheaders",
    "django_filters",
    "django_celery_beat",
]

CUSTOM_APPS = ["users", "skills", "jobs", "ratings", "interviews"]

# final list of APPS
INSTALLED_APPS = DJANGO_CORE_APPS + THIRD_PARTY_APPS + CUSTOM_APPS


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "imt_mng.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / "templates"],
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

WSGI_APPLICATION = "imt_mng.wsgi.application"


# Database
DATABASES = {
    "local": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent.parent / "local.sqlite3",
    },
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DATABASE_NAME", default="mydb"),
        "USER": os.getenv("POSTGRES_USER", default="myuser"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", default="mypassword"),
        "HOST": os.getenv("POSTGRES_HOST", default="localhost"),
        "PORT": os.getenv("POSTGRES_PORT", default="5432"),
    },
}

# Dynamically set the default database based on DJANGO_ENV
DATABASES["default"] = DATABASES.get(ENVIRONMENT, DATABASES["default"])

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# Internationalization
LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

# This is from where collectstatic command would collect all static files
STATICFILES_DIRS = [
    BASE_DIR / "static",
]
STATIC_URL = "static/"

# This is  where collectstatic command would PLACE all collected static files from STATICFILES_DIRS
STATIC_ROOT = BASE_DIR / "static"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# User model declaration
AUTH_USER_MODEL = "users.User"

# *********** Phone number settings *************
PHONENUMBER_DEFAULT_REGION = "AT"  # Default region for numbers without a country code
PHONENUMBER_DB_FORMAT = "E164"  # Store phone numbers in E.164 format
PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"  # Format for display
# ********************************************
# Celery settings
CELERY_BROKER_URL = 'redis://redis:6379/0'

# ****** Django authentication settings ******
## Redirect after successful login
LOGIN_REDIRECT_URL = "/users/home"

# Redirect to login page if not authenticated
LOGIN_URL = "/users/login/"
# ********************************************

# STATIC files settings.
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR.parent / "static"]
# ********************************************

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
}

SPECTACULAR_SETTINGS = {
    "TITLE": "IMT Apis",
    "DESCRIPTION": "Interview Management Tool",
    "VERSION": "0.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

# JWT settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
}

# Logger settings
handlers =  {
    "local": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": BASE_DIR.parent.parent / "logs" /"debug.log",
            "formatter": "my_formatter",
        },
    }, 
    "default": {
        "console": {
            "class": "logging.StreamHandler",
        },     
    },
    "testing": {
        "console": {
            "class": "logging.StreamHandler",
        },     
    },
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "my_formatter": {
            "format": "%(asctime)s, File: %(module)s.py, Message: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": handlers[ENVIRONMENT],
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "imt": {
            "handlers": ["file"] if ENVIRONMENT == "local" else ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "users": {
            "handlers": ["file"] if ENVIRONMENT == "local" else ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}