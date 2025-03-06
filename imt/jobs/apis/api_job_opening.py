from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from jobs.models import JobOpening
from jobs.serializers import JobOpeningSerializer
from drf_spectacular.utils import extend_schema
import django_filters


class JobOpeningFilter(django_filters.FilterSet):
    """This sets up rules for filterinf Job Openings."""
    status = django_filters.ChoiceFilter(
        choices=JobOpening.status_choices,
        field_name="status",
        empty_label=None,  # Ensures users must pick from the choices
    )

    job_type = django_filters.MultipleChoiceFilter(
        choices=JobOpening.JOB_TYPE_CHOICES,
        field_name="job_type",
    )

    class Meta:
        model = JobOpening
        fields = ["position", "status", "city", "job_type"]

    @property
    def qs(self):
        """Apply default filters unless explicitly overridden"""
        queryset = super().qs

        # Allow users to request all statuses by passing "all"
        status_value = self.data.get("status")
        if not status_value:
            queryset = queryset.filter(status="O")  # Default: Open jobs
        elif status_value.lower() == "all":
            pass  # Do nothing, keep all statuses
        else:
            queryset = queryset.filter(status=status_value)

        # Allow users to request all job types by passing "all"
        job_type_value = self.data.get("job_type")
        if not job_type_value:
            queryset = queryset.filter(job_type="P")  # Default: Permanent jobs
        elif job_type_value.lower() == "all":
            pass  # Do nothing, keep all job types
        else:
            queryset = queryset.filter(job_type__in=job_type_value.split(","))
        return queryset


@extend_schema(
    tags=["Job Opening"],
)
class JobOpeningViewSet(viewsets.ModelViewSet):
    """
    Viewset for job openings.
    """

    queryset = JobOpening.objects.select_related("position")
    serializer_class = JobOpeningSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter] # Enables filtering
    filterset_class = JobOpeningFilter # Defines how filtering works

    def get_queryset(self):
        queryset = super().get_queryset()
        position_id = self.request.query_params.get("position")

        if position_id:
            queryset = queryset.filter(position_id=position_id)

        return queryset
