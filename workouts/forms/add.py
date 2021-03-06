from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.forms.widgets import DateTimeInput
from django.shortcuts import get_object_or_404

from dal import autocomplete

from workouts.models import WorkoutSet, Workout, Exercise, Hold, Hangboard
from climbers.models import Climber, Preference, Measurement


class AddWorkoutForm(ModelForm):

    name = forms.CharField(strip=True, required=False)
    logged = forms.DateTimeField(initial=timezone.now(), widget=DateTimeInput)

    class Meta:
        model = Workout
        fields = (
            'hangboard',
            'name',
            'logged',
        )
        widgets = {
            'hangboard': autocomplete.ModelSelect2(url='workouts:autocomplete_hangboard')
        }


class AddWorkoutSetForm(ModelForm):

    weight = forms.IntegerField()
    rest_between = forms.IntegerField()
    rest_after = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(AddWorkoutSetForm, self).__init__(*args, **kwargs)
        initial = kwargs.get('initial', None)
        climber = Climber.objects.get(pk=initial['climber'])
        preference = Preference.objects.get(pk=climber.pk)
        measurement = Measurement.objects.get(pk=climber.pk)
        workout = Workout.objects.get(pk=initial['workout'])
        workout_sets = workout.get_workout_sets()
        hold_set = workout.hangboard.hold_set
        exercises = Exercise.objects.all()

        if workout_sets and initial['previous']:
            previous = WorkoutSet.objects.get(pk=initial['previous'])
            self.fields['exercise'] = forms.ModelChoiceField(queryset=exercises, initial=previous.exercise)
            self.fields['weight'] = forms.IntegerField(initial=previous.weight)
            self.fields['rest_between'] = forms.IntegerField(initial=previous.rest_between)
            self.fields['rest_after'] = forms.IntegerField(initial=previous.rest_after)
            self.fields['left_hold'] = forms.ModelChoiceField(queryset=hold_set, initial=previous.left_hold)
            self.fields['right_hold'] = forms.ModelChoiceField(queryset=hold_set, initial=previous.right_hold)
        else:
            self.fields['weight'] = forms.IntegerField(initial=measurement.get_current_weight())
            self.fields['rest_between'] = forms.IntegerField(initial=preference.rest_between)
            self.fields['left_hold'] = forms.ModelChoiceField(queryset=hold_set)
            self.fields['right_hold'] = forms.ModelChoiceField(queryset=hold_set)
            self.fields['rest_after'] = forms.IntegerField(initial=preference.rest_after)

    class Meta:
        model = WorkoutSet
        fields = (
            'exercise',
            'left_hold',
            'left_fingers',
            'right_hold',
            'right_fingers',
            'duration',
            'rest_after',
        )
        widgets = {
            'exercise': autocomplete.ModelSelect2(url='workouts:autocomplete_exercise'),
            'left_hold': autocomplete.ModelSelect2(url='workouts:autocomplete_hold'),
        }


class AddHoldForm(ModelForm):

    class Meta:
        model = Hold
        fields = (
            'name',
            'description',
            'hold_type',
            'hangboard',
            'size',
            'angle',
            'max_fingers',
            'position_id',
            'position',
            'climber',

        )
        widgets = {
            'hold_type': autocomplete.ModelSelect2(url='workouts:autocomplete_hold_type')
        }