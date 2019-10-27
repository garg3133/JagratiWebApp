from django.urls import path
from .views import login_signup, logout_fun

urlpatterns = [
    path('', login_signup, name = 'login_signup'),
    path('logout/', logout_fun, name = 'logout'),
]