from django.db import models
from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from interviews.models import InterviewRound


class AspectTemplate(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, default="")
    expected_points = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class RatingSheetTemplate(models.Model):
    name = models.CharField(max_length=100)
    rate_min = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    rate_max = models.IntegerField(default=6, validators=[MaxValueValidator(100)])
    aspects = models.ManyToManyField(
        to=AspectTemplate, related_name="aspects", blank=True
    )

    def __str__(self):
        return self.name


class InterviewRoundRatingSheet(models.Model):
    name = models.CharField(max_length=200, default="MySheet")
    round = models.ForeignKey(InterviewRound, null=True, on_delete=models.CASCADE)
    comment = models.TextField(default="", blank=True)

    def __str__(self):
        return self.name


class RatingAspect(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField(null=True, default="", blank=True)
    round_rating_sheet = models.ForeignKey(
        InterviewRoundRatingSheet, on_delete=models.CASCADE
    )
    points = models.PositiveIntegerField(default=0)
    expected_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
