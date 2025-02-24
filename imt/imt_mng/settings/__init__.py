import os
from django.core.exceptions import ImproperlyConfigured


# Get the environment name (e.g., 'local', 'default', 'test')
ENVIRONMENT = os.getenv("DJANGO_ENV", default="local")

if not ENVIRONMENT:
    raise ImproperlyConfigured("DJANGO_ENV environment variable is not set!")

if ENVIRONMENT == "local":
    from .local import *
elif ENVIRONMENT == "default":
    from .production import *
elif ENVIRONMENT == "testing":
    from .testing import *
else:
    raise ImproperlyConfigured(f"Unknown DJANGO_ENV: {ENVIRONMENT}")

# Load the appropriate settings file
from .log_settings import *