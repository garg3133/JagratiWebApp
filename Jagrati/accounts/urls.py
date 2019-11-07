from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_signup, name = 'login_signup'),
    path('logout/', views.logout_view, name = 'logout'),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]