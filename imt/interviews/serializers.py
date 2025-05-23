from rest_framework import serializers
from .models import InterviewFeedback, InterviewRound
from jobs.serializers import MinimalJobApplicationSerializer


class InterviewRoundSerializer(serializers.ModelSerializer):
    application = MinimalJobApplicationSerializer()

    class Meta:
        model = InterviewRound
        fields = [
            "id",
            "duration_in_mins",
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
