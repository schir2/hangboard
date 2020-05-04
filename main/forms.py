from django.forms import ModelForm
from django import forms
from django.utils.text import slugify

from main.models import WorkoutSet, Workout
from climbers.models import Climber, Profile, Preference, Measurement


class WorkoutSetForm(ModelForm):

    def __init__(self,user, *args, **kwargs):
        super(WorkoutSetForm, self).__init__(*args, **kwargs)
        climber = Climber.objects.get(pk=user.pk)
        preference = Preference.objects.get(pk=climber.pk)
        measurement = Measurement.objects.get(pk=climber.pk)
        workout = Workout.objects.filter(climber=climber.pk).latest()
        workout_sets = workout.workoutset_set.all()
        hold_set = workout.hangboard.hold_set
        self.fields['workout'] = forms.IntegerField(initial=workout.pk, disabled=True)
        self.fields['climber'] = forms.CharField(initial=climber.pk, disabled=True)
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

    def save(self, *args, **kwargs):
        if not self.left_hold and not self.right_hold:
            raise ValueError('No holds selected')
        if not self.left_hold:
            self.left_fingers = None

        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        if not self.description:
            self.description = self.name
        super().save(*args, *kwargs)


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