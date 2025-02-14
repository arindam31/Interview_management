import random
import datetime
from faker import Faker

from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand
from django.utils import timezone


from users.models import Candidate, Staff, User
from jobs.models import JobOpening, JobApplication
from interviews.models import InterviewRound

fake = Faker()


class Command(BaseCommand):
    help = "Generate some candidates."

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **options):
        all_candidates = Candidate.objects.all()
        all_openings = JobOpening.objects.all()
        me_user, created = User.objects.get_or_create_staff(username="test_staff")
        if me_user:
            me_staff, _ = Staff.objects.get_or_create(user=me_user, first_name="Staff_fname")
        else:
            print("Failed to create applications as no Staff user found")

        for _ in range(options["num"]):
            candidate = random.choice(all_candidates)
            job_opening = random.choice(all_openings)
            job_application = JobApplication.objects.create(
                candidate=candidate, opening=job_opening
            )
            try:
                int_rnd = InterviewRound.objects.create(
                    application=job_application,
                    scheduled_at=timezone.make_aware(
                        random.choice(
                            [
                                datetime.datetime.today() + datetime.timedelta(days=d)
                                for d in range(1, 14)
                            ]
                        )
                    ),
                    result=fake.random_element(elements=("A", "F", "N")),
                )
            except ValidationError:
                print("candidate has interview already booked.")
            except Exception:
                print("something else did not work.")
                raise

            try:
                int_rnd.interviewers.set([me_staff])
                print("Create application")
            except ValidationError:
                continue
