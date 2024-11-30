from django.http import HttpResponse
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
import logging
from .models import Staff

logger = logging.getLogger("users")


class HomepageView(TemplateView):
    template_name = "home.html"


class UserLoginView(LoginView):
    template_name = "users/login.html"
