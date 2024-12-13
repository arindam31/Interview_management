from rest_framework import serializers
from .models import JobPosition, JobApplication, JobOpening
from skills.models import Skill
from skills.serializers import SkillSerializer


class JobPositionSerializer(serializers.ModelSerializer):
    required_skills = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skill.objects.all()
    )
    optional_skills = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Skill.objects.all()
    )
    required_skills_detail = SkillSerializer(
        many=True, read_only=True, source="required_skills"
    )
    optional_skills_detail = SkillSerializer(
        many=True, read_only=True, source="optional_skills"
    )

    class Meta:
        model = JobPosition
        fields = [
            "id",
            "title",
            "job_company_id",
            "min_exp_needed_in_years",
            "description",
            "required_skills",
            "optional_skills",
            "required_skills_detail",
            "optional_skills_detail",
        ]


class JobOpeningSerializer(serializers.ModelSerializer):
    position = serializers.PrimaryKeyRelatedField(queryset=JobPosition.objects.all())
    position_details = JobPositionSerializer(read_only=True, source="position")

    class Meta:
        model = JobOpening
        fields = [
            "id",
            "position",
            "position_details",
            "city",
            "posted_date",
            "closing_date",
            "job_type",
            "status",
        ]
        read_only_fields = ["posted_date"]


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = [
            "id",
            "candidate",
            "opening",
            "applied_on",
            "comments",
            "final_result",
            "status",
        ]
