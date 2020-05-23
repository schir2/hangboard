from django.urls import path, include
from climbers.views import profile_view

urlpatterns = [
    path('<str:username>/', profile_view),
    path('<str:username>/profile/', profile_view, name='profile_view'),
    path('<str:username>/workouts/', include('workouts.urls')),
]