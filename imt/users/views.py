from django.shortcuts import redirect
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView
import logging
from .models import Staff

logger = logging.getLogger("users")


class HomepageView(TemplateView):
    template_name = "home.html"


class UserLoginView(LoginView):
    template_name = "users/login.html"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")  # Redirect to the home page if logged in
        return super().get(request, *args, **kwargs)
