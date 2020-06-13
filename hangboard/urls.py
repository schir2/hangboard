from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('climber/', include('climbers.urls')),
    path('workouts/', include('workouts.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
