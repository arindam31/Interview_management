import uuid
from phonenumber_field.modelfields import PhoneNumberField

# local imports
from skills.models import Skill

# Django imports
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.contrib.auth.password_validation import validate_password
from django.db import models


class TimestampedModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# Custom User Manager
class UserManager(BaseUserManager):
    def create(self, *args, **kwargs):
        """Block create() default method so no one can mistakenly use that.
        If one did use that, there will be no error.
        But the user cannot login since password won't be hashed.
        """
        raise NotImplementedError(
            "Directly calling 'create()' is not allowed. Please use one of the following methods instead: "
            "create_user(), create_superuser(), create_staff(), create_regular_user()."
        )

    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("The Username field is required")

        if password:
            validate_password(password)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Create a super user"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        
        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_staff=True and is_superuser=True.")
        
        return self.create_user(username, password, **extra_fields)

    def create_staff(self, username, password=None, **extra_fields):
        """This user is a staff and can login to admin."""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(username, password, **extra_fields)

    def create_regular_user(self, username, password=None, **extra_fields):
        """This user cannot login to admin."""
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self.create_user(username, password, **extra_fields)

    def get_or_create_staff(self, **kwargs):
        """
        Get or create a staff user.
        Assumes staff status is required for the user.
        """
        kwargs.setdefault("is_staff", True)
        user, created = self.get_or_create(**kwargs)
        return user, created

    def get_or_create_superuser(self, **kwargs):
        """
        Get or create a superuser.
        Assumes superuser status is required.
        """
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_staff", True)
        user, created = self.get_or_create(**kwargs)
        return user, created

    def get_or_create_regular_user(self, **kwargs):
        """
        Get or create a user object for anyone who is NOT staff.
        You dont want him to login on admin.
        """
        kwargs.setdefault("is_superuser", False)
        kwargs.setdefault("is_staff", False)
        user, created = self.get_or_create(**kwargs)
        return user, created


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

    def __str__(self):
        return f"{self.first_name}_{self.last_name}"


class Candidate(TimestampedModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="candidate"
    )
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    primary_phone_number = PhoneNumberField(blank=True, region="AT")
    city = models.CharField(max_length=200)
    resume = models.FileField(upload_to="resumes/", blank=True)
    skills = models.ManyToManyField(to=Skill, related_name="candidates", blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
