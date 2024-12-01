import environ
from pathlib import Path

# Setup env
env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False),
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
env_file = BASE_DIR.parent / ".env"
environ.Env.read_env(str(env_file))

# False if not in os.environ
DEBUG = env("DEBUG")
SECRET_KEY = env("SECRET_KEY")
ENVIRONMENT = env("DJANGO_ENV", default="local")
print(f"ENVIRONMENT used is : {ENVIRONMENT}")

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


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
    "cities_light",
    "phonenumber_field",
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
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent.parent / "imt.sqlite3",
    },
    "production": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", default="mydb"),
        "USER": env("POSTGRES_USER", default="myuser"),
        "PASSWORD": env("POSTGRES_PASSWORD", default="mypassword"),
        "HOST": env("POSTGRES_HOST", default="localhost"),
        "PORT": env("POSTGRES_PORT", default="5432"),
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
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# User model declaration
AUTH_USER_MODEL = "users.User"

# *********** Phone number settings *************
PHONENUMBER_DEFAULT_REGION = "AT"  # Default region for numbers without a country code
PHONENUMBER_DB_FORMAT = "E164"  # Store phone numbers in E.164 format
PHONENUMBER_DEFAULT_FORMAT = "INTERNATIONAL"  # Format for display
# ********************************************


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
