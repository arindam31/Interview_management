from django.urls import path, include
from users.apis.api_auth import CustomTokenApi


# JWT token apis
urlpatterns = [
    path(
        "token/",
        CustomTokenApi.as_view(),
        name="custom_token_obtain_pair",
    ),
]
