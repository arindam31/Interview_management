import os
from django.core.exceptions import ImproperlyConfigured

# Get the environment name (e.g., 'local', 'prod', 'test')
ENVIRONMENT = os.getenv("DJANGO_ENV", default="local")

if not ENVIRONMENT:
    raise ImproperlyConfigured("DJANGO_ENV environment variable is not set!")

# Load the appropriate settings file
if ENVIRONMENT == "local":
    from .local import *
elif ENVIRONMENT == "production":
    from .production import *
elif ENVIRONMENT == "testing":
    from .testing import *
else:
    raise ImproperlyConfigured(f"Unknown DJANGO_ENV: {ENVIRONMENT}")
