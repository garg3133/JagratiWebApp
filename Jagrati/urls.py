from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Jagrati Admin"
admin.site.site_title = "Jagrati Admin Portal"
admin.site.index_title = "Welcome to Jagrati Administration"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('students/', include('apps.students.urls')),
    path('volunteers/', include('apps.volunteers.urls')),
    path('feedbacks/', include('apps.feedbacks.urls')),

    # Rest API URLs
    path('api/', include('home.api.urls')),
    path('api/accounts/', include('accounts.api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
