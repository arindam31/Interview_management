import random
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Staff, User
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ValidationError

# local imports
from tests.conftest import get_authenticated_client
from jobs.models import JobPosition, JobOpening, JobApplication
from skills.models import Skill
from users.models import Candidate, User
from interviews.models import InterviewRound


class TestInterviewRoundApis(APITestCase):
    def setUp(self):
        self.username = "TestUser"
        self.password = "!!_&Bogus321&_!!"
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
        # This returns the authenticated client
        self.client = get_authenticated_client(self.username, self.password)

    def test_api_get_list_or_rounds(self):
        # url = "http://127.0.0.1:8000/interviews/api/interview-rounds/"
        url = reverse("interviewround-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class TestInterviewRoundConflicts(APITestCase):
    def setUp(self):
        self.username = "TestUser"
        self.password = "Bogus$321"
        self.staff_user = User.objects.create_staff(
            username=self.username, password=self.password
        )
        self.staff_user_other = User.objects.create_staff(
            username="OtherGuy", password=self.password
        )
        self.staff: Staff = Staff.objects.create(
            first_name="S1",
            last_name="last_name",
            user=self.staff_user,
            email="staff@mail.com",
            department="HR",
        )
        self.staff_other: Staff = Staff.objects.create(
            first_name="S2",
            last_name="last_name_other",
            user=self.staff_user_other,
            email="staff@mail2.com",
            department="HR",
        )
        # This returns the authenticated client
        self.client = get_authenticated_client(self.username, self.password)
        job_position = JobPosition.objects.create(
                    title="Senior Associate",
                    job_company_id="SA")
        cities = ("Vienna", "Salzburg", "Innsbruck", "Graz", "Klagenfurth")
        job_opening = JobOpening.objects.create(position=job_position, city=random.choice(cities))
        skills = ["Python", "BackEnd", "Java", "Test Automation", "Finance"]

        for skill in skills:
            Skill.objects.get_or_create(name=skill)
        skills = Skill.objects.all()

        user = User.objects.create_regular_user(
                username="candiname", password="TestPass@12345"
            )
        candi = Candidate.objects.create(
                user=user,
                first_name="Candi Fname",
                last_name="Candi Lname",
                email="mail@candi.com",
                primary_phone_number="1234567890",
                city="FakeCity",
            )
        a_skill = random.choice(skills)
        candi.skills.add(a_skill)

        self.job_application = JobApplication.objects.create(
                candidate=candi, opening=job_opening
            )
        