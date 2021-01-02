from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.index_new, name='index_new'),
    path('old/', views.index, name='index_old'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/update_cwhw/', views.update_cwhw, name='update_cwhw'),
    path('ajax/dashboard/', views.ajax_dashboard, name='ajax_dashboard'),
]