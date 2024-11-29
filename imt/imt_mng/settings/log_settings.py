import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
logs_dir = BASE_DIR.parent.parent / "logs"
logs_dir.mkdir(parents=True, exist_ok=True)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "my_formatter": {
            "format": "%(asctime)s, File: %(module)s.py, Function: %(funcName)s, Message: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": logs_dir / "debug.log",
            "formatter": "my_formatter",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "imt": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
        "users": {
            "handlers": ["file"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
