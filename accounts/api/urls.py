from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration_view, name='api_register'),
    path('login/', views.LoginView.as_view(), name='api_login'),
    path('complete_profile/',
         views.complete_profile_view,
         name='api_complete_profile'),
    path('logout/', views.LogoutView.as_view(), name='api_logout'),
    path('check_login_status/',
         views.check_login_status,
         name='api_check_login_status'),
]
