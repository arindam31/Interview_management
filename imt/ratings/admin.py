from django.contrib import admin
from .models import (
    AspectTemplate,
    RatingSheetTemplate,
    InterviewRoundRatingSheet,
    RatingAspect,
)


@admin.register(RatingAspect)
class RatingAspectAdmin(admin.ModelAdmin):
    list_display = ("name", "points", "expected_points")


@admin.register(InterviewRoundRatingSheet)
class InterviewRoundRatingAdmin(admin.ModelAdmin):
    list_display = ("name", "round")


@admin.register(RatingSheetTemplate)
class RatingSheetTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "rate_min", "rate_max")


@admin.register(AspectTemplate)
class AspectTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "expected_points")
