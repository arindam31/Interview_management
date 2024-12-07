from django.core.management.base import BaseCommand
from faker import Faker
from skills.models import Skill

fake = Faker()


class Command(BaseCommand):
    help = "Generate some skills"

    def handle(self, *args, **kwargs):
        skills = ["Python", "BackEnd", "Java", "Test Automation", "Finance"]

        for skill in skills:
            Skill.objects.get_or_create(name=skill)
