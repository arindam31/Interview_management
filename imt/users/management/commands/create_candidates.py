import random
from django.core.management.base import BaseCommand
from faker import Faker
from users.models import Candidate, User
from skills.models import Skill

fake = Faker()


class Command(BaseCommand):
    help = "Generate some candidates."

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **options):
        list_candi = []
        all_skills = Skill.objects.all()

        for _ in range(options["num"]):
            user = User.objects.create_regular_user(
                username=fake.user_name(), password=fake.password()
            )
            candi = Candidate.objects.create(
                user=user,
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                primary_phone_number=fake.phone_number(),
                city=fake.city(),
            )
            a_skill = random.choice(all_skills)
            candi.skills.add(a_skill)

        print(f"Created {options['num']} candidate objects.")
