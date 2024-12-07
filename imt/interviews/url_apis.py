from django.urls import path, include
from rest_framework import routers
from .apis.api_interview_round import InterviewRoundViewSet
from .apis.api_interview_feedback import InterviewFeedbackViewSet

router = routers.DefaultRouter()

# Note: We need to provide a basename as we have not provided a queryset in the API viewset.
router.register(r"interview-rounds", InterviewRoundViewSet, basename="interviewround")
router.register(
    r"interview-feedbacks", InterviewFeedbackViewSet, basename="interviewfeedback"
)


urlpatterns = [
    path("", include(router.urls)),
]
