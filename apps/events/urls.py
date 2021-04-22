from django.urls import path

from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('event_all/', views.events_all, name='events_all'),
    path('add/', views.add_event, name='add_event'),
]
