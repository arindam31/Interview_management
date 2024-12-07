from django.db import models

# local imports
from skills.models import Skill
from users.models import Candidate


class JobPosition(models.Model):
    title = models.CharField(max_length=100, unique=True)
    job_company_id = models.CharField(max_length=10, unique=True)
    min_exp_needed_in_years = models.PositiveIntegerField(default=0)
    description = models.TextField()
    required_skills = models.ManyToManyField(
        Skill, related_name="required_for_positions"
    )
    optional_skills = models.ManyToManyField(
        Skill, related_name="optional_for_positions", blank=True
    )

    def __str__(self):
        return self.title


class JobOpening(models.Model):
    """An opening is a job advertisement taken out by the company,
    against which people can submit a JobApplication.

    Conditions:
    - An opening should never be deleted if it has at least, one application. It can only be closed.
    - We can never have more than one job opening for the same position and city (we used constraints to check that.)
    """

    position = models.ForeignKey(
        JobPosition, on_delete=models.CASCADE, related_name="job_openings"
    )
    city = models.CharField(max_length=200)

    posted_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField(blank=True, null=True)
    JOB_TYPE_CHOICES = (
        ("P", "Permanent"),
        ("T", "Temporary"),
        ("I", "Intern"),
    )
    job_type = (
        models.CharField(  # This field can be shown in template as get_status_display
            max_length=1, choices=JOB_TYPE_CHOICES, default="P"
        )
    )
    status_choices = (
        ("O", "Open"),
        ("C", "Closed"),
    )
    status = models.CharField(max_length=1, choices=status_choices, default="O")

    def delete(self, *args, **kwargs):
        if self.job_applications.exists():
            raise ValueError(
                "Cannot delete a job opening with associated applications. Close the job opening instead."
            )
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"{self.position.title} in {self.city if self.city else 'Unknown'}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["position", "city"],
                condition=models.Q(status="O"),
                name="unique_job_opening_per_position_city",
            )
        ]


class JobApplication(models.Model):
    candidate = models.ForeignKey(
        to=Candidate,
        related_name="job_applications",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    opening = models.ForeignKey(
        to=JobOpening, related_name="job_applications", on_delete=models.PROTECT
    )
    applied_on = models.DateField(auto_now_add=True)
    STATE_CHOICES = (
        ("O", "Open"),
        ("P", "In Progress"),
        ("C", "Closed"),
    )
    FINAL_RESULT_CHOICES = (
        ("SJ", "Selected Joined"),
        ("SNJ", "Selected Did Not Join"),
        ("NS", "Not Selected"),
        ("C", "Cancelled"),
        ("P", "Pending"),
    )
    comments = models.CharField(max_length=250, blank=True)
    status = models.CharField(max_length=1, choices=STATE_CHOICES, default="O")
    final_result = models.CharField(
        max_length=3, choices=FINAL_RESULT_CHOICES, default="P"
    )

    def __str__(self):
        return f"Application by {self.candidate} for {self.opening.position.title}"
