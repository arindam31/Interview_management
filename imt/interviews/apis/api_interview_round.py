from datetime import date
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.utils.dateparse import parse_date

# local imports
from interviews.models import InterviewRound
from interviews.serializers import InterviewRoundSerializer


@extend_schema(
    tags=["Interview Rounds"],
)
class InterviewRoundViewSet(viewsets.ModelViewSet):
    serializer_class = InterviewRoundSerializer

    def get_queryset(self):
        application_id = self.request.query_params.get("application_id")

        if self.action == "list":
            if application_id:
                try:
                    # Ensure application_id is an integer
                    application_id = int(application_id)
                    queryset = InterviewRound.objects.filter(
                        application_id=application_id
                    )
                    if not queryset.exists():
                        raise ValidationError(
                            {
                                "application_id": "No records found for the provided application ID."
                            }
                        )
                    return queryset
                except ValueError:
                    raise ValidationError(
                        {
                            "application_id": "Invalid application ID. Must be an integer."
                        }
                    )
            else:
                return InterviewRound.objects.order_by("-scheduled_at")[:10]

        # Default for other actions (`retrieve`, `update`, `delete`, etc.)
        return InterviewRound.objects.all()

    @extend_schema(
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
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="staff_id",
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                description="Filter interview rounds by application ID.",
            ),
            OpenApiParameter(
                name="start_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="Start range of round.",
            ),
            OpenApiParameter(
                name="end_date",
                type=OpenApiTypes.DATE,
                location=OpenApiParameter.QUERY,
                description="End range of round.",
            ),
        ],
        description="List interview rounds by staff assigned and date range.",
    )
    @action(detail=False, methods=["get"])
    def interviewer_rounds(self, request):
        """
        Custom action to get interview rounds for a specific staff and date range.
        """
        staff_id = request.query_params.get("staff_id")
        start_date = request.query_params.get("start_date", date.today().isoformat())
        end_date = request.query_params.get(
            "end_date", start_date
        )  # Default to the same day

        try:
            # Parse dates
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)

            if not start_date or not end_date:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")

            if not staff_id:
                raise ValidationError({"staff_id": "Staff ID is required."})

            rounds = InterviewRound.objects.filter(
                interviewers__id__in=[staff_id],
                scheduled_at__date__range=[start_date, end_date],
            )

            if not rounds.exists():
                return Response(
                    {"message": "No interview rounds found for the given criteria."},
                    status=404,
                )

            serializer = self.get_serializer(rounds, many=True)
            return Response(serializer.data)

        except ValueError as e:
            raise ValidationError({"error": str(e)})
