import logging
from django.db import transaction, IntegrityError
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from .models import Candidate, Staff, User
from skills.models import Skill
from skills.serializers import SkillSerializer

logger = logging.getLogger("users")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        try:
            staff = Staff.objects.get(user_id=self.user.id)
            data["staff_id"] = str(staff.id)
        except Staff.DoesNotExist:
            logger.info("No staff found...only user object present.")
        return data


class CandidateSerializer(serializers.ModelSerializer):
    skills = serializers.PrimaryKeyRelatedField(many=True, queryset=Skill.objects.all())

    skill_details = SkillSerializer(many=True, read_only=True, source="skills")
    resume = serializers.FileField(use_url=True)
    primary_phone_number = PhoneNumberField()

    class Meta:
        model = Candidate
        fields = [
            "id",
            "created_at",
            "updated_at",
            "first_name",
            "last_name",
            "email",
            "primary_phone_number",
            "city",
            "resume",
            "skills",
            "skill_details",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "is_staff", "is_active"]


class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = [
            "id",
            "user",
            "created_at",
            "updated_at",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
        ]

    def generate_random_password(self, length=12):
        import secrets
        import string
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(length))

    def create(self, validated_data):
        email:str = validated_data.get("email")
        if not email:
            serializers.ValidationError({"error":"Email is missing"})
        
        username =  email.split("@")[0]

        # generate a random password.
        pwd = self.generate_random_password()

        # all or nothing
        try:
            with transaction.atomic():
                user =  User.objects.create_staff(username=username, password=pwd)
                staff = Staff.objects.create(user=user, **validated_data)
            return staff
        except IntegrityError:
            raise serializers.ValidationError("Failed to create Staff due to incorrect input. Please check")


class StaffDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Staff
        fields = [
            "id",
            "created_at",
            "updated_at",
            "user",
            "first_name",
            "last_name",
            "email",
            "phone",
            "department",
        ]
