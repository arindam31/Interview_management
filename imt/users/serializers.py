from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Candidate
from skills.models import Skill
from skills.serializers import SkillSerializer
from phonenumber_field.serializerfields import PhoneNumberField


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data["id"] = self.user.id  # Example: add user role to the token
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
