from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import UserLoginView, HomepageView

urlpatterns = [
    path("home", HomepageView.as_view(template_name="home.html"), name="home"),
    path(
        "login/", UserLoginView.as_view(template_name="users/login.html"), name="login"
    ),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
]
