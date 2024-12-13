from django.test import TestCase

from jobs.models import JobPosition
from jobs.serializers import (
    JobPositionSerializer,
)
from skills.models import Skill
from skills.serializers import SkillSerializer


class TestJobPositionSerializer(TestCase):

    def setUp(self):
        self.skill_01 = Skill.objects.create(name="TestSkill")
        self.skill_02 = Skill.objects.create(name="TestSkill_2")
        self.job_pos = JobPosition.objects.create(
            title="TestPosition",
            job_company_id="TP01",
            min_exp_needed_in_years=3,
            description="Test details for job position",
        )
        self.job_pos.required_skills.add(self.skill_01)
        self.job_pos.required_skills.add(self.skill_02)

    def test_serializer_response(self):
        expected = {
            "id": self.job_pos.id,
            "title": self.job_pos.title,
            "job_company_id": self.job_pos.job_company_id,
            "min_exp_needed_in_years": self.job_pos.min_exp_needed_in_years,
            "description": self.job_pos.description,
            "required_skills": [
                self.skill_01.id,
                self.skill_02.id,
            ],
            "required_skills_detail": [
                SkillSerializer(self.skill_01).data,
                SkillSerializer(self.skill_02).data,
            ],
            "optional_skills_detail": [],
            "optional_skills": [],
        }
        serialized_data = JobPositionSerializer(self.job_pos)
        self.assertEqual(serialized_data.data, expected)

    def test_create_using_serializer(self):
        """Test to verify POST behavior when all params are valid"""

        params = {
            "title": "new_position",
            "job_company_id": "ABC123",
            "min_exp_needed_in_years": 5,
            "description": "test description",
            "required_skills": [self.skill_01.id],
            "optional_skills": [self.skill_02.id],
        }
        serializer_obj = JobPositionSerializer(data=params)
        self.assertTrue(serializer_obj.is_valid())

    def test_create_using_serializer_invalid_skill_id(self):
        """Test to verify POST behavior when a skill id is invalid"""
        params = {
            "title": "new_position",
            "job_company_id": "ABC123",
            "min_exp_needed_in_years": 5,
            "description": "test description",
            "required_skills": [999],
            "optional_skills": [self.skill_02.id],
        }
        serializer_obj = JobPositionSerializer(data=params)
        self.assertFalse(serializer_obj.is_valid())
        self.assertEqual(
            serializer_obj.errors,
            {"required_skills": ['Invalid pk "999" - object does not exist.']},
        )

    def test_read_only_fields(self):
        """Input data without the `id` field (read-only fields should not be in input)"""
        data = {
            "title": "Updated Title",
            "job_company_id": "SE123",
            "min_exp_needed_in_years": 3,
            "description": "Test description",
            "required_skills": [self.skill_01.id],
            "optional_skills": [self.skill_02.id],
        }
        serializer = JobPositionSerializer(data=data)

        # Assert the serializer is valid
        self.assertTrue(serializer.is_valid())

        # Ensure the validated data does not include read-only fields
        self.assertNotIn("id", serializer.validated_data)

    def test_title_max_length(self):
        data = {
            "title": "x" * 101,  # Exceeding max length of 100
            "job_company_id": "SE123",
            "min_exp_needed_in_years": 3,
            "description": "Test",
        }
        serializer = JobPositionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("title", serializer.errors)
