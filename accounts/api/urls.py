from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration_view, name='api_register'),
    path('login/', views.LoginView.as_view(), name='api_login'),
]