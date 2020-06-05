from django.urls import path, include

from workouts.views.add import add_workout_set_view
from workouts.views.add import add_workout_view
from workouts.views.add import add_exercise_view
from workouts.views.add import add_hangboard_view
from workouts.views.add import AddMaterialView

from workouts.views.edit import edit_exercise_view

from workouts.views.get import WorkoutListView
from workouts.views.get import workout_detail_view
from workouts.views.get import hangboard_detail_view
from workouts.views.get import WorkoutSetDetailView
from workouts.views.get import ExerciseListView
from workouts.views.get import HangboardListView
from workouts.views.get import HoldListView
from workouts.views.get import MaterialListView

urlpatterns = [
    path('', WorkoutListView.as_view(), name='workout_list'),
    path('exercises', ExerciseListView.as_view(), name='exercise_list'),
    path('hangboards', HangboardListView.as_view(), name='hangboard_list'),
    path('hangboards/hangboard=<int:hangboard_id>/', hangboard_detail_view, name='hangboard_detail'),
    path('materials', MaterialListView.as_view(), name='material_list'),

    path('add_exercise', add_exercise_view, name='add_exercise'),
    path('add_workout', add_workout_view, name='add_workout'),
    path('add_hangboard', add_hangboard_view, name='add_hangboard'),
    path('add_material', AddMaterialView.as_view(), name='add_material'),

    path('edit_exercise/<int:exercise_id>/', edit_exercise_view, name='edit_exercise'),

    path('workout=<int:workout_id>/', workout_detail_view, name='workout_detail'),
    path('workout=<int:workout_id>/workout_set=<int:workout_set_id>', WorkoutSetDetailView.as_view(), name='workout_set_detail'),
    path('workout=<int:workout_id>/add/', add_workout_set_view, name='add_workout_set'),
    path('workout=<int:workout_id>/add/previous=<int:previous>', add_workout_set_view, name='add_workout_set')
]