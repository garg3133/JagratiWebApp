from django.urls import path
from . import views

urlpatterns =[
    path('', views.index, name='home'),
    path('dashboard/', views.dashboard, name = 'dashboard'),
    path('set_profile/', views.volunteerInformation, name='set_profile'),
]