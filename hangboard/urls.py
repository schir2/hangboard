from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('climber/', include('climbers.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
