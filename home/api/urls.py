from django.urls import path
from . import views

urlpatterns = [
    path("create_profile/", views.create_profile_view, name="api_create_profile"),
    path("update_profile/", views.update_profile_view, name="api_update_profile"),
]
