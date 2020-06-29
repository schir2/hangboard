from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('main.urls')),
    path('accounts/', include(('allauth.urls','allauth'), namespace='allauth')),
    path('admin/', admin.site.urls),
    path('blog/', include(('blog.urls', 'blog'), namespace='blog')),
    path('climber/', include(('climbers.urls','climbers'),namespace='climbers')),
    path('workouts/', include(('workouts.urls', 'workouts'),namespace='workouts')),
    path('ckeditor/', include(('ckeditor_uploader.urls','ckeditor'),namespace='ckeditor')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
