from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Candidate, Staff
from skills.models import Skill
from skills.serializers import SkillSerializer
from phonenumber_field.serializerfields import PhoneNumberField
import logging

logger = logging.getLogger("users")


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id
        try:
            staff = Staff.objects.get(user_id=self.user.id)
            data["staff_id"] = staff.id
        except Staff.DoesNotExist:
            logger.info("No staff found...onle user object present.")
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


class StaffSerializer(serializers.ModelSerializer):
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
