from django.db import models
from django.utils import timezone
from jobs.models import JobApplication


class InterviewRound(models.Model):
    """An Interview round is a process where the candidate is evaluaed for some skill(s)

    The round can be organized using various means:
    - telephonic
    - video call
    - written exam
    - in person (face-to-face)

    The result of a Round, can be
    - advancing to next round (if there are more lined-up)
    - exiting from the round ending his application.
    """

    application = models.ForeignKey(
        JobApplication, on_delete=models.CASCADE, related_name="interview_rounds"
    )
    round_type_choices = (
        ("T", "Telephonic"),
        ("V", "Video"),
        ("W", "Written"),
        ("F", "Face-to-Face"),
    )
    round_type = models.CharField(max_length=1, choices=round_type_choices, default="T")
    interviewers = models.ManyToManyField(
        "users.Staff", related_name="interview_rounds", blank=True
    )
    scheduled_at = models.DateTimeField()
    result_choices = (
        ("A", "Advanced"),
        ("F", "Fail"),
        ("N", "No Decision"),
    )
    result = models.CharField(max_length=1, choices=result_choices, default="N")
    next_round = models.OneToOneField(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="prev_round",
    )

    def __str__(self):
        return f"Round {self.type} for {self.application.candidate}"

    @classmethod
    def interviews_today(cls):
        return cls.objects.filter(date=timezone.datetime.today())


class InterviewFeedback(models.Model):
    round = models.ForeignKey(
        InterviewRound, on_delete=models.CASCADE, related_name="feedback_entries"
    )
    interviewer = models.ForeignKey(
        "users.Staff", on_delete=models.CASCADE, related_name="feedback_entries"
    )
    comments = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (
            "round",
            "interviewer",
        )  # Ensure one feedback per interviewer per round

    def __str__(self):
        return f"Feedback by {self.interviewer} for {self.round}"
