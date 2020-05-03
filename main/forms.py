from django.forms import ModelForm
from django import forms

from main.models import Hangboard
from main.models import Hold
from main.models import Exercise
from main.models import WorkoutSet
from main.models import Workout
from django.contrib.auth import get_user_model


class WorkoutSetForm(ModelForm):

    def __init__(self, climber, *args, **kwargs):
        super(WorkoutSetForm, self).__init__(*args, **kwargs)
        self.fields['workout'] = forms.ModelChoiceField(
            queryset=Workout.objects.filter(climber=climber)
        )


    class Meta:
        model = WorkoutSet
        fields = ('created',)
        exclude = (
            'slug',
            'description',
            'name',
            'workout',
            'completed',
            'custom',
            'climber',
        )