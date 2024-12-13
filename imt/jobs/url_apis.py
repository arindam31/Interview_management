from rest_framework.routers import DefaultRouter
from .apis.api_job_position import JobPositionViewSet

router = DefaultRouter()
router.register(r"job-positions", JobPositionViewSet, basename="job-position")

urlpatterns = router.urls
