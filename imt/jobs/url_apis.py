from rest_framework.routers import DefaultRouter
from .apis.api_job_position import JobPositionViewSet
from .apis.api_job_opening import JobOpeningViewSet

router = DefaultRouter()
router.register(r"job-positions", JobPositionViewSet, basename="job-position")
router.register(r"job-openings", JobOpeningViewSet, basename="job-opening")

urlpatterns = router.urls
