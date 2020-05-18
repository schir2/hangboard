from django.urls import path

from main.views.add import add_workout_set_view
from main.views.add import add_workout_view
from main.views.get import WorkoutListView
from main.views.get import workout_detail_view
from main.views.get import WorkoutSetDetailView

urlpatterns = [
    path('forms/workout_set/<int:workout_id>', add_workout_set_view, name='add_workout_set'),
    path('forms/workout_set/<int:workout_id>/<int:previous>', add_workout_set_view, name='add_workout_set'),
    path('forms/add_workout', add_workout_view, name='add_workout'),
    path('', WorkoutListView.as_view(), name='workout_list'),
    path('<slug:slug>/', workout_detail_view, name='workout_detail'),
    path('<slug:workout_slug>/set=<int:position>', WorkoutSetDetailView.as_view(), name='workout_set_detail'),
]