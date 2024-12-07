from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter


# local imports
from interviews.serializers import InterviewFeedbackSerializer
from interviews.models import InterviewFeedback


@extend_schema(
    tags=["Interview Feedback"],
    parameters=[
        OpenApiParameter(
            name="round_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Filter interview feedbacks by round ID.",
        )
    ],
    description="List interview feedbacks. Optionally filter by round ID. "
    "If `round_id` is not provided, the latest 10 interview feedbacks are returned.",
)
class InterviewFeedbackViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewFeedbackSerializer

    def get_queryset(self):
        round_id = self.request.query_params.get("round_id")

        if round_id:
            try:
                return InterviewFeedback.objects.filter(round_id=round_id)
            except ValueError:
                raise ValidationError({"round_id": "Invalid round_id."})
        else:
            return InterviewFeedback.objects.all()[:10]
