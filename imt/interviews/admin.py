from django.contrib import admin
from .models import InterviewFeedback, InterviewRound


@admin.register(InterviewFeedback)
class InterviewFeedbackAdmin(admin.ModelAdmin):
    pass


@admin.register(InterviewRound)
class InterviewRoundAdmin(admin.ModelAdmin):
    pass
