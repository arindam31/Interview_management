# myapp/management/commands/generate_mock_data.py
from datetime import datetime, timedelta
from random import choice, randrange
from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker

# local imports
from users.models import Candidate, User, Staff
from jobs.models import JobOpening, JobApplication, JobPosition
from interviews.models import InterviewRound
from skills.models import Skill


fake = Faker()


class Command(BaseCommand):
    help = "Generate mock data for testing"

    def handle(self, *args, **kwargs):
        list_position = [
            "Test Engineer",
            "Senior BackEnd Developer",
            "FrontEnd Developer",
            "Assistant HR",
        ]

        all_skills = Skill.objects.all()
        all_staff = Staff.objects.all()

        for pos in list_position:
            job_pos, _ = JobPosition.objects.get_or_create(
                title=pos, defaults={"title": pos, "job_company_id": randrange(1, 100)}
            )
            job_pos.required_skills.add(choice(all_skills))

        # Generate Job Openings
        job_positions = JobPosition.objects.all()
        for _ in range(10):
            job, _ = JobOpening.objects.get_or_create(
                position=choice(job_positions),
                city=fake.city(),
                defaults={"position": choice(job_positions), "city": fake.city()},
            )

            # Generate Candidates and Application Processes
            for _ in range(5):
                user, _ = User.objects.get_or_create_regular_user(
                    username=fake.user_name()
                )
                candidate, _ = Candidate.objects.get_or_create(
                    user=user,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    email=fake.email(),
                    primary_phone_number=fake.phone_number(),
                    city=fake.city(),
                )
                candidate.skills.add(choice(all_skills))
                job_application = JobApplication.objects.create(
                    candidate=candidate, opening=job
                )

                for i in range(1, 4):  # Simulating multiple interview rounds
                    interview_round = InterviewRound.objects.create(
                        application=job_application,
                        result=fake.random_element(elements=("A", "F", "N")),
                        scheduled_at=timezone.make_aware(
                            choice(
                                [
                                    datetime.today() + timedelta(days=d)
                                    for d in range(1, 31)
                                ]
                            )
                        ),
                    )
                    interview_round.interviewers.add(choice(all_staff))
        self.stdout.write(self.style.SUCCESS("Mock data generated successfully!"))
