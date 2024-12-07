import pytest
from django.test import TestCase
from users.models import Staff
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class TestUserManager(TestCase):
    """Test the user custom manager methods for our custom User"""

    def setUp(self):
        self.username = "TestUser"
        self.password = "Bogus$321"
        self.staff_user = User.objects.create_staff(
            username=self.username, password=self.password
        )
        self.staff: Staff = Staff.objects.create(
            first_name="S1",
            last_name="last_name",
            user=self.staff_user,
            email="staff@mail.com",
            department="HR",
        )

    def test_create_staff(self):
        """Test creating a staff user."""
        user = User.objects.create_staff(
            username="staff_user", password="staffpassword"
        )
        assert user.username == "staff_user"
        assert user.is_staff is True
        assert user.is_superuser is False
        assert user.check_password(
            "staffpassword"
        )  # Password should be hashed and verified

    def test_create_regular_user(self):
        """Test creating a general user."""
        user = User.objects.create_regular_user(
            username="general_user", password="generalpassword"
        )
        assert user.username == "general_user"
        assert user.is_staff is False
        assert user.is_superuser is False
        assert user.check_password(
            "generalpassword"
        )  # Password should be hashed and verified

    def test_create_with_missing_username(self):
        """Test creating a user without a username raises an error."""
        with pytest.raises(ValueError, match="The Username field is required"):
            User.objects.create_staff(username=None, password="testpassword")

    def test_user_login_valid_credentials(self):
        """Test for valid credentials"""
        logged_in_user = authenticate(username=self.username, password=self.password)
        if logged_in_user is None:
            self.fail("Staff unable to login")

    def test_create_method_must_not_be_enabled(self):
        """Test if someone uses user.objects.create(), it must not work, since this will lead to issues."""
        with self.assertRaisesMessage(
            NotImplementedError,
            "Directly calling 'create()' is not allowed. Please use one of the following methods instead: "
            "create_user(), create_superuser(), create_staff(), create_regular_user().",
        ):
            User.objects.create(username=self.username, password=self.password)
