from django.urls import path, include
from climbers.views import profile_view
from climbers.views import preferences_view
from climbers.views import measurements_view

urlpatterns = [
    path('profile/', profile_view, name='profile'),
    path('preferences/', preferences_view, name='preferences'),
    path('measurements/', measurements_view, name='measurements'),
]