from django.urls import path, include

from workouts.views.add import add_workout_set_view
from workouts.views.add import add_workout_view
from workouts.views.get import WorkoutListView
from workouts.views.get import workout_detail_view
from workouts.views.get import WorkoutSetDetailView

urlpatterns = [
    path('', WorkoutListView.as_view(), name='workout_list'),
    path('add_workout', add_workout_view, name='add_workout'),
    path('workout=<int:workout_id>/', workout_detail_view, name='workout_detail'),
    path('workout=<int:workout_id>/workout_set=<int:workout_set_id>', WorkoutSetDetailView.as_view(), name='workout_set_detail'),
    path('workout=<int:workout_id>/add/', add_workout_set_view, name='add_workout_set'),
    path('workout=<int:workout_id>/add/previous=<int:previous>', add_workout_set_view, name='add_workout_set')
]