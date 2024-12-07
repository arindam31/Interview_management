from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

# local imports
from interviews.models import InterviewRound
from interviews.serializers import InterviewRoundSerializer


@extend_schema(
    tags=["Interview Rounds"],
    parameters=[
        OpenApiParameter(
            name="application_id",
            type=OpenApiTypes.INT,
            location=OpenApiParameter.QUERY,
            description="Filter interview rounds by application ID.",
        )
    ],
    description="List interview rounds. Optionally filter by application ID. "
    "If `application_id` is not provided, the latest 10 interview rounds are returned.",
)
class InterviewRoundViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewRoundSerializer

    def get_queryset(self):
        application_id = self.request.query_params.get("application_id")

        if application_id:

            try:
                # Ensure application_id is an integer
                application_id = int(application_id)
                queryset = InterviewRound.objects.filter(application_id=application_id)
                if not queryset.exists():
                    raise ValidationError(
                        {
                            "application_id": "No records found for the provided application ID."
                        }
                    )
                return queryset
            except ValueError:
                raise ValidationError(
                    {"application_id": "Invalid application ID. Must be an integer."}
                )
        else:
            return InterviewRound.objects.order_by("-scheduled_at")[:10]
