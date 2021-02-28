from django.urls import path

from . import views

app_name = 'feedbacks'
urlpatterns = [
    path('', views.index, name='index'),
    path('submitted/', views.feedback_submitted, name='feedback_submitted'),
]
