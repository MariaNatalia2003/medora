from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.doctor_register, name="register"),
    path("login/", views.doctor_login, name="login"),
    path("logout/", views.doctor_logout, name="logout"),
    path("dashboard/", views.doctor_dashboard, name="doctor_dashboard"),
]
