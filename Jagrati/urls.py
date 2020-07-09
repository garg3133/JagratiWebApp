from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Jagrati Admin"
admin.site.site_title = "Jagrati Admin Portal"
admin.site.index_title = "Welcome to Jagrati Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),

    # Rest API URLs
    path('api/accounts/', include('accounts.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
