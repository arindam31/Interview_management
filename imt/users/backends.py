from django.contrib.auth.backends import BaseBackend


class StaffBackend(BaseBackend):
    """Allow staff to login with username or email"""

    pass
