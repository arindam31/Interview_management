import uuid
from cities_light.models import City
from phonenumber_field.modelfields import PhoneNumberField

# Django imports
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


class TimestampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Custom User Manager
class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, password, **extra_fields)

    def create_staff(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(username, password, **extra_fields)

    def create_general_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(username, password, **extra_fields)


# Custom User Model
class User(AbstractBaseUser, PermissionsMixin, TimestampedModel):
    username = models.CharField(max_length=150, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Required for admin access

    objects = UserManager()

    USERNAME_FIELD = "username"  # Primary login field
    REQUIRED_FIELDS = []  # No additional fields are required

    def __str__(self):
        return self.username


class Staff(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="staff")
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    department = models.CharField(max_length=100, blank=True)


class Candidate(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="candidate"
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    primary_phone_number = PhoneNumberField(blank=True, region="AT")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    resume = models.FileField(upload_to="resumes/", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
