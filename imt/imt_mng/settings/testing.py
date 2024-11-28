from .base import *

DEBUG = False

# Use an in-memory database for faster tests (SQLite)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Disable any debug mode for speed
DEBUG = False

# Use fast password hashing for user tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]


class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return "notmigrations"


MIGRATION_MODULES = DisableMigrations()
