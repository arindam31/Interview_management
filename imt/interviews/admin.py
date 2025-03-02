from django.contrib import admin
from .models import InterviewFeedback, InterviewRound


@admin.register(InterviewFeedback)
class InterviewFeedbackAdmin(admin.ModelAdmin):
    pass


@admin.register(InterviewRound)
class InterviewRoundAdmin(admin.ModelAdmin):
    list_display = ["scheduled_at", "get_round_type", "application"]
    
    def get_round_type(self, obj):
        return obj.get_round_type_display()
