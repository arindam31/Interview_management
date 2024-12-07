from .models import InterviewFeedback, InterviewRound
from rest_framework import serializers


class InterviewRoundSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewRound
        fields = [
            "application",
            "round_type",
            "interviewers",
            "scheduled_at",
            "result",
            "next_round",
        ]


class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = "__all__"
