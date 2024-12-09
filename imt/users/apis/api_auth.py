from users.serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class CustomTokenApi(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
