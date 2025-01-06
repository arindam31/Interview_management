from drf_spectacular.utils import extend_schema

from rest_framework import viewsets
from rest_framework.response import Response

# local imports
from users.models import Staff
from users.serializers import StaffSerializer, StaffDetailsSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


@extend_schema(
    tags=["Staff"],
)
class StaffViewset(viewsets.ModelViewSet):
    queryset = Staff.objects.all().order_by("-created_at")
    serializer_class = StaffDetailsSerializer
    filterset_fields = ["user__is_active"]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = StaffDetailsSerializer(instance)
        return Response(serializer.data)
