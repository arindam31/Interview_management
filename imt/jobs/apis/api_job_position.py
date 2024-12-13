from rest_framework import viewsets
from jobs.models import JobPosition
from jobs.serializers import JobPositionSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter


@extend_schema(
    tags=["Job Position"],
)
class JobPositionViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions (list, create, retrieve, update, destroy)
    for the JobPosition model.
    """

    queryset = JobPosition.objects.prefetch_related(
        "required_skills", "optional_skills"
    )
    serializer_class = JobPositionSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned job positions to those matching query parameters,
        such as title or company ID.
        """
        queryset = super().get_queryset()
        title = self.request.query_params.get("title")
        job_company_id = self.request.query_params.get("job_company_id")

        if title:
            queryset = queryset.filter(title__icontains=title)
        if job_company_id:
            queryset = queryset.filter(job_company_id=job_company_id)

        return queryset
