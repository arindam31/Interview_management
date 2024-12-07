from datetime import timedelta
from .models import InterviewRound
from users.models import Staff


def get_available_interviewers(scheduled_at):
    conflicting_interviewers = InterviewRound.objects.filter(
        scheduled_at__range=(
            scheduled_at - timedelta(minutes=15),
            scheduled_at + timedelta(minutes=15),
        )
    ).values_list("interviewers", flat=True)

    available_interviewers = Staff.objects.exclude(id__in=conflicting_interviewers)
    return available_interviewers
