import pytest
from django.test import TestCase
from users.models import Staff
from users.views import StaffView
from django.conf import settings
from django.contrib.auth import get_user_model


class UserViewTest(TestCase):
    def setUp(self):
        user = get_user_model()
        self.user = user.objects.create(username="TestUser", password="Bogus$321")
        self.staff = Staff.objects.create(first_name="S1", user=self.user)

    def test_staff(self):
        self.assertEqual(1, 1)
