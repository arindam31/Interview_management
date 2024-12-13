from django.test import TestCase
from django.utils import timezone

from jobs.models import JobPosition, JobOpening
from jobs.serializers import (
    JobOpeningSerializer,
    JobPositionSerializer,
)
from skills.models import Skill


class TestJobOpeningSerializer(TestCase):

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
        self.job_opening = JobOpening.objects.create(
            position=self.job_pos, city="Mycity", job_type="P"
        )

    def test_serializer_response(self):
        expected = {
            "id": self.job_opening.id,
            "position_details": JobPositionSerializer(self.job_pos).data,
            "position": self.job_pos.id,
            "city": self.job_opening.city,
            "job_type": "P",
            "status": "O",
            "posted_date": str(timezone.datetime.today().date()),
            "closing_date": None,
            "status": "O",
        }
        serialized_data = JobOpeningSerializer(self.job_opening)
        self.assertEqual(serialized_data.data, expected)

    def test_create_using_serializer(self):
        """Test to verify POST behavior when all params are valid"""

        params = {
            "position": self.job_pos.id,
            "city": "ABC123",
        }
        serializer_obj = JobOpeningSerializer(data=params)
        self.assertTrue(serializer_obj.is_valid())

    def test_create_using_serializer_invalid_position_id(self):
        """Test to verify POST behavior when a position id is invalid"""
        params = {
            "position": 999,
            "city": "ABC123",
        }
        serializer_obj = JobOpeningSerializer(data=params)
        self.assertFalse(serializer_obj.is_valid())
        self.assertEqual(
            serializer_obj.errors,
            {"position": ['Invalid pk "999" - object does not exist.']},
        )

    def test_read_only_fields(self):
        """Input data without the `id` field (read-only fields should not be in input)"""
        params = {
            "position": self.job_pos.id,
            "city": "ABC123",
            "posted_date": str(timezone.datetime.today().date()),
        }
        serializer = JobOpeningSerializer(data=params)

        # Assert the serializer is valid
        self.assertTrue(serializer.is_valid())

        # Ensure the validated data does not include read-only fields
        self.assertNotIn("id", serializer.validated_data)
        self.assertNotIn("posted_date", serializer.validated_data)
