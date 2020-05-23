from django.urls import path, include
from climbers.views import profile_view
from climbers.views import preferences_view
from climbers.views import measurements_view

urlpatterns = [
    path('<str:username>/', profile_view),
    path('<str:username>/profile/', profile_view, name='profile'),
    path('<str:username>/profile/', preferences_view, name='preferences'),
    path('<str:username>/profile/', measurements_view, name='measurements'),
    path('<str:username>/workouts/', include('workouts.urls')),
]