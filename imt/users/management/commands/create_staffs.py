from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from users.models import Staff, User


fake = Faker()


class Command(BaseCommand):
    help = "Generate some staff members"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **options):
        # accept number of staffs needed to be created

        list_staff = []
        for _ in range(options["num"]):
            user = User.objects.create_staff(
                username=fake.user_name(), password=fake.password()
            )
            staff = Staff(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                phone=fake.phone_number(),
            )
            list_staff.append(staff)

        Staff.objects.bulk_create(list_staff)
        print(f"Created {options['num']} staff objects.")
