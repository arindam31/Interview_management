import pytest
from django.test import TestCase
from users.models import Staff
from users.views import StaffView
from django.conf import settings


class UserViewTest(TestCase):
    def setUp(self):
        self.staff = Staff.objects.create(first_name="S1")

    def test_staff(self):
        pass
