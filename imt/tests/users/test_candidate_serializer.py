from faker import Faker
from django.contrib.auth import get_user_model
from django.test import TestCase

# local imports
from users.serializers import CandidateSerializer
from users.models import Candidate
from skills.models import Skill
from skills.serializers import SkillSerializer


User = get_user_model()
fake = Faker()


class TestCandidateSerializer(TestCase):

    def setUp(self):
        self.password = "Bogus$321"
        self.skill_01 = Skill.objects.create(name="TestSkill")
        self.skill_02 = Skill.objects.create(name="TestSkill_2")

        self.user = User.objects.create_regular_user(
            username="Candi", password=self.password
        )
        self.candidate = Candidate.objects.create(
            user=self.user,
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            primary_phone_number="+911234598745",
            city=fake.city(),
            resume=None,
        )
        self.candidate.skills.add(self.skill_01, self.skill_02)

    def test_is_valid(self):
        """Test if valid object is used."""

        expected = {
            "id": str(self.candidate.id),
            "first_name": self.candidate.first_name,
            "last_name": self.candidate.last_name,
            "email": self.candidate.email,
            "primary_phone_number": str(self.candidate.primary_phone_number),
            "city": self.candidate.city,
            "skill_details": [
                SkillSerializer(self.skill_01).data,
                SkillSerializer(self.skill_02).data,
            ],
            "skills": [self.skill_01.id, self.skill_02.id],
            "resume": None,
        }

        serialized_data = CandidateSerializer(self.candidate).data
        self.assertIn("created_at", serialized_data)
        self.assertIn("updated_at", serialized_data)

        del serialized_data["created_at"]
        del serialized_data["updated_at"]

        self.assertEqual(serialized_data, expected)
