import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from jobs.models import JobOpening, JobPosition
from skills.models import Skill


class Command(BaseCommand):
    help = "Generate some positions."

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **options):
        titles = (
            "Test Engineer",
            "Backend Developer",
            "Front Dev",
            "Devops Engineer",
            "Test Manager",
        )
        skills = Skill.objects.all()

        for _ in range(options["num"]):
            title = random.choice(titles)
            try:
                jo = JobPosition.objects.create(
                    title=title,
                    job_company_id="".join(
                        list(map(lambda word: word[0], title.split()))
                    ),
                    min_exp_needed_in_years=3,
                )
                jo.required_skills.add(random.choice(skills))
                jo.optional_skills.add(random.choice(skills))
            except IntegrityError:
                print("Opening exists for city and position.")
            except Exception:
                print("something else did not work.")
                