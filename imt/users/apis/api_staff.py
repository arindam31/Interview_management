from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter

from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination

# local imports
from users.models import Staff
from users.serializers import StaffSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@extend_schema(
    tags=["Staff"],
)
class StaffViewset(viewsets.ModelViewSet):
    queryset = Staff.objects.all().order_by("-created_at")
    serializer_class = StaffSerializer
