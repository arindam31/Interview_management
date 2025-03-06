from datetime import datetime
from faker import Faker
from django.contrib.auth import get_user_model
from django.test import TestCase

# local imports
from users.models import Staff
from users.serializers import StaffDetailsSerializer, StaffSerializer, UserSerializer



User = get_user_model()
fake = Faker()


class TesStaffSerializer(TestCase):

    def setUp(self):
        self.password = "Bogus$321"
        
        self.user = User.objects.create_staff(
            username="iamstaff", password=self.password
        )
        self.staff =  Staff.objects.create(user=self.user, first_name="S_fname", last_name="s_lname", email="staff@mail.com", phone="+4367763712345", department="HR")

    def test_valid_single_staff(self):
        
        created_at = f"{self.staff.created_at.time().hour}:{self.staff.created_at.time().minute}:{self.staff.created_at.time().second}"
        updated_at = f"{self.staff.updated_at.time().hour}:{self.staff.updated_at.time().minute}:{self.staff.updated_at.time().second}"
        expected = {
            "id": str(self.staff.id),
            "first_name": self.staff.first_name,
            "last_name": self.staff.last_name,
            "email": self.staff.email,
            "phone": str(self.staff.phone),
            "created_at": created_at,
            "updated_at": updated_at,
            "department": self.staff.department,
            "user": UserSerializer(self.user).data,
        }
         
        serialized_data = StaffDetailsSerializer(self.staff).data
        created_at_rec = datetime.strptime(serialized_data["created_at"], "%Y-%m-%dT%H:%M:%S.%f%z").time()
        updated_at_rec = datetime.strptime(serialized_data["updated_at"], "%Y-%m-%dT%H:%M:%S.%f%z").time()
        created_time_serialized = f"{created_at_rec.hour}:{created_at_rec.minute}:{created_at_rec.second}"
        updated_time_serialized = f"{updated_at_rec.hour}:{updated_at_rec.minute}:{updated_at_rec.second}"
        serialized_data["created_at"] = created_time_serialized
        serialized_data["updated_at"] = updated_time_serialized
        self.assertEqual(serialized_data, expected)