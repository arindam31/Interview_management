from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

# local imports
from users.models import Candidate
from users.serializers import CandidateSerializer


class CandidatePagination(PageNumberPagination):
    page_size = 10  # Default page size
    page_size_query_param = "page_size"  # Allow users to override the page size
    max_page_size = 50  # Max page size, cannot exceed 50 candidates


@extend_schema(
    tags=["Candidate"],
)
class CandidateViewset(viewsets.ModelViewSet):
    queryset = Candidate.objects.all().order_by("-created_at")
    serializer_class = CandidateSerializer
    pagination_class = CandidatePagination
    filter_backends = (SearchFilter,)
    search_fields = ["first_name", "last_name", "email"]

    def get_queryset(self):
        """
        Optionally restricts the returned candidates to the latest N (default 10),
        or based on query parameters like page_size.
        """
        queryset = super().get_queryset()

        # If 'page_size' is provided, use it. Otherwise, default to 10 per page.
        page_size = self.request.query_params.get("page_size", 10)
        if page_size:
            page_size = min(int(page_size), self.pagination_class.max_page_size)

        self.pagination_class.page_size = page_size
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="page_size",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                description="Get by page_size.",
            )
        ],
        description="Get List of candidates..by default you get 10 sorted by created_at",
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
