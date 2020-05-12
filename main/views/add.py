from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from main.forms import AddWorkoutForm
from main.forms import AddWorkoutSetForm

from main.models import Workout
from main.models import WorkoutSet


@login_required
def add_workout_view(request, *args, **kwargs):
    template_name = 'main/forms/add_workout.html'
    context = dict()
    context['title'] = 'Add Workout'
    if request.method == 'POST':
        context['form'] = AddWorkoutForm(request.POST)
        if context['form'].is_valid():
            workout = Workout.objects.add_workout(
                climber=request.user,
                **context['form'].cleaned_data
            )
            return redirect('workout_detail', slug=workout.slug)
        else:
            raise ValueError('Invalid Form Values')
    else:
        context['form'] = AddWorkoutForm()
    return render(request, template_name=template_name, context=context)


@login_required
def add_workout_set_view(request, workout, previous=None):
    template_name = 'main/forms/add_workout_set.html'
    context = dict()
    context['title'] = 'Add Workout Set'
    if request.method == 'POST':
        context['form'] = AddWorkoutSetForm(request.POST)
        if context['form'].is_valid():
            workout_set = WorkoutSet.objects.add_workout_set(
                climber=request.user,
                workout=workout,
                previous=previous,
                **context['form'].cleaned_data
            )
            return redirect('workout_detail', slug=workout.slug)
        else:
            raise ValueError('Invalid Form Values')
    else:
        context['form'] = AddWorkoutSetForm()

    return render(request, template_name=template_name, context=context)
