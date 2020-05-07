from django.urls import path

from main.views import workout_set_form_view
from main.views import WorkoutListView
from main.views import WorkoutDetailView

urlpatterns = [
    path('forms/workout_set', workout_set_form_view, name='workout_set_form'),
    path('', WorkoutListView.as_view(), name='workout_list'),
    path('<slug:slug>/', WorkoutDetailView.as_view(), name='workout_detail'),
]