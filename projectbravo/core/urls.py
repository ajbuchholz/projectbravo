from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("dashboard/", TemplateView.as_view(template_name="home.html"), name="dashboard"),
    path("accounts/", include("apps.accounts.urls")),
]
