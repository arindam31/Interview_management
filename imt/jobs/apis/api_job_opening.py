from rest_framework import viewsets
from jobs.models import JobOpening
from jobs.serializers import JobOpeningSerializer
from drf_spectacular.utils import extend_schema


@extend_schema(
    tags=["Job Opening"],
)
class JobOpeningViewSet(viewsets.ModelViewSet):
    """
    Viewset for job openings.
    """

    queryset = JobOpening.objects.prefetch_related("position")
    serializer_class = JobOpeningSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        position_id = self.request.query_params.get("position")

        if position_id:
            queryset = queryset.filter(position_id=position_id)

        return queryset
