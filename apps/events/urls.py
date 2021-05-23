from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_event, name='add_event'),
    path('captures/', views.captures, name='captures'),
]
