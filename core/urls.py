from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("services/", views.services, name="services"),
    path("thank-you/", views.thank_you, name="thank_you"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/request/<int:request_id>/", views.request_detail, name="request_detail"),
]