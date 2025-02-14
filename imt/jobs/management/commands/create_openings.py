import random

from django.core.management.base import BaseCommand
from django.db import IntegrityError
from jobs.models import JobOpening, JobPosition


class Command(BaseCommand):
    help = "Generate some openings."

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **options):
        all_positions = JobPosition.objects.all()
        if not all_positions:
            raise Exception("no positions exists. create some")

        cities = ("Vienna", "Salzburg", "Innsbruck", "Graz", "Klagenfurth")
        
        for _ in range(options["num"]):
            job_position = random.choice(all_positions)
            try:
                jo = JobOpening.objects.create(position=job_position, city=random.choice(cities))
            except IntegrityError:
                print("Opening exists for city and position.")
            except Exception as e:
                print(f"something else did not work. {e}")
                