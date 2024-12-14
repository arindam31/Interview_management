from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.apis.api_auth import CustomTokenApi
from users.apis.api_candidate import CandidateViewset
from users.apis.api_staff import StaffViewset


router = DefaultRouter()
router.register(r"candidate", CandidateViewset, basename="candidate")
router.register(r"staff", StaffViewset, basename="staff")

urlpatterns = router.urls


# JWT token apis
urlpatterns = [
    path(
        "token/",
        CustomTokenApi.as_view(),
        name="custom_token_obtain_pair",
    ),
]

# Add the router URLs to the urlpatterns
urlpatterns += router.urls
