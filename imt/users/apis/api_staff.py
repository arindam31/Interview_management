from drf_spectacular.utils import extend_schema

from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

# local imports
from users.models import Staff
from users.serializers import StaffSerializer, StaffDetailsSerializer


class StaffPagination(PageNumberPagination):
    page_size = 10 


@extend_schema(
    tags=["Staff"],
)
class StaffViewset(viewsets.ModelViewSet):
    queryset = Staff.objects.select_related("user").order_by("-created_at")
    serializer_class = StaffDetailsSerializer
    pagination_class = StaffPagination
    filterset_fields = ["user__is_active"]

    def get_serializer_class(self):
        """Use different serializers for list and retrieve actions."""
        if self.action == "list":
            return StaffSerializer
        return StaffDetailsSerializer

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
