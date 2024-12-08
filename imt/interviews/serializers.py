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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["round_type"] = instance.get_round_type_display()
        return representation


class InterviewFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = InterviewFeedback
        fields = "__all__"
