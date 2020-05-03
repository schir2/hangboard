from django.urls import path

from main.views import workout_set_form_view

urlpatterns = [
    path('forms/workout_set', workout_set_form_view, name='workout_set_form'),
]