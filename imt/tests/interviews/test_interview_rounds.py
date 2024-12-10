from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Staff, User
from tests.conftest import get_authenticated_client
from django.urls import reverse


class TestInterviewRoundApis(APITestCase):
    def setUp(self):
        self.username = "TestUser"
        self.password = "Bogus$321"
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
