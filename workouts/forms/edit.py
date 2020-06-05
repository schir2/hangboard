from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.forms.widgets import DateTimeInput

from workouts.models import WorkoutSet, Workout, Exercise, Hangboard
from climbers.models import Climber, Preference, Measurement


class EditExerciseForm(ModelForm):
    
    def save(self, climber=None):
        exercise = super(EditExerciseForm, self).save(commit=False)
        if climber:
            exercise.climber = climber
        exercise.save()
        return exercise

    class Meta:
        model = Exercise
        fields = (
            'id',
            'name',
        )

"""
class EditHangboardForm(ModelForm):

    class Meta:
        model = Hangboard
        fields = (
            'pk',
            'name',
            'material',
            'climber',
        )
"""