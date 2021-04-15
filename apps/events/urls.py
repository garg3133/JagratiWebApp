from django.contrib import admin
from django.urls import path
from django.conf import settings 
from django.conf.urls.static import static 
 
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_event, name='add_event'),
 path('show_event/<int:myid>',views.show_event,name='show_event'),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)