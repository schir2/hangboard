from django.forms import ModelForm
from django import forms
from django.utils import timezone
from django.forms.widgets import DateTimeInput

from main.models import WorkoutSet, Workout
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


class AddWorkoutSetForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddWorkoutSetForm, self).__init__(*args, **kwargs)
        climber = Climber.objects.get(pk=args[0]['climber'])
        preference = Preference.objects.get(pk=climber.pk)
        measurement = Measurement.objects.get(pk=climber.pk)
        workout = Workout.objects.filter(pk=args[0]['workout']).latest()
        workout_sets = workout.workoutset_set.all()
        hold_set = workout.hangboard.hold_set
        if workout_sets:
            latest_workout_set = workout_sets.latest()
            self.fields['exercise'] = forms.IntegerField(initial=latest_workout_set.exercise)
            self.fields['position'] = forms.IntegerField(initial=latest_workout_set.position)
            self.fields['weight'] = forms.IntegerField(initial=latest_workout_set.weight)
            self.fields['rest_between'] = forms.IntegerField(initial=latest_workout_set.rest_between)
            self.fields['rest_after'] = forms.IntegerField(initial=latest_workout_set.rest_after)
            self.fields['left_hold'] = forms.ModelChoiceField(queryset=hold_set)
            self.fields['right_hold'] = forms.ModelChoiceField(queryset=hold_set)
        else:
            self.fields['position'] = forms.IntegerField(initial=0)
            self.fields['weight'] = forms.IntegerField(initial=measurement.get_current_weight())
            self.fields['rest_between'] = forms.IntegerField(initial=preference.rest_between)
            self.fields['rest_after'] = forms.IntegerField(initial=preference.rest_after)
            self.fields['left_hold'] = forms.ModelChoiceField(queryset=hold_set)
            self.fields['right_hold'] = forms.ModelChoiceField(queryset=hold_set)

    class Meta:
        model = WorkoutSet
        fields = (
            'exercise',
            'weight',
            'reps',
            'duration', 'rest_between',
            'left_hold',
            'left_fingers',
            'right_hold',
            'right_fingers',

        )
        exclude = (
            'slug',
            'description',
            'name',
            'workout',
            'completed',
            'custom',
            'climber',
            'workout',
        )