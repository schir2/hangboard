from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from workouts.forms import AddWorkoutForm
from workouts.forms import AddWorkoutSetForm
from workouts.forms import AddExerciseForm
from workouts.forms import AddHangboardForm

from workouts.models import Workout
from workouts.models import WorkoutSet


@login_required
def add_workout_view(request, *args, **kwargs):
    template_name = 'workouts/add/workout.html'
    context = dict()
    context['title'] = 'Add Workout'
    if request.method == 'POST':
        context['form'] = AddWorkoutForm(request.POST)
        if context['form'].is_valid():
            workout = Workout.objects.add_workout(
                climber=request.user,
                **context['form'].cleaned_data
            )
            return redirect('workout_detail', workout_id=workout.id, username=request.user.username)
        else:
            raise ValueError('Invalid Form Values')
    else:
        context['form'] = AddWorkoutForm()
    return render(request, template_name=template_name, context=context)


@login_required
def add_workout_set_view(request, workout_id, username, previous=None, *args, **kwargs):
    template_name = 'workouts/add/workout_set.html'
    context = dict()
    context['title'] = 'Add Workout Set'
    workout = Workout.objects.get(pk=workout_id)
    initial_fields = {
        'workout': workout_id,
        'climber': request.user.pk,
        'previous': previous,
    }
    if request.method == 'POST':
        context['form'] = AddWorkoutSetForm(request.POST, initial=initial_fields)
        previous = WorkoutSet.objects.get(pk=previous) if previous else None
        if context['form'].is_valid():
            workout_set = WorkoutSet.objects.add_workout_set(
                climber=request.user,
                workout=workout,
                previous=previous,
                **context['form'].cleaned_data
            )
            workout_set.save()
            return redirect('workout_detail', workout_id=workout.pk, username=username)
        else:
            raise ValueError('Invalid Form Values')
    else:
        context['form'] = AddWorkoutSetForm(initial=initial_fields)

    return render(request, template_name=template_name, context=context)


@login_required
def add_exercise_view(request, username, *args, **kwargs):
    template_name = 'workouts/add/exercise.html'
    context = dict()
    context['title'] = 'Add Exercise'
    initial_fields = {'climber': request.user.pk}
    if request.method == 'POST':
        context['form'] = AddExerciseForm(request.POST, initial=initial_fields)
        if context['form'].is_valid():
            context['form'].save()
    else:
        context['form'] = AddExerciseForm(initial=initial_fields)
    return render(request, template_name=template_name, context=context)


@login_required
def add_hangboard_view(request, username, *args, **kwargs):
    template_name = 'workouts/add/hangboard.html'
    context = dict()
    context['title'] = 'Add Hangboard'
    initial_fields = {'climber': request.user.pk}
    if request.method == 'POST':
        context['form'] = AddHangboardForm(request.POST, initial=initial_fields)
        if context['form'].is_valid():
            hangboard = context['form'].save()
            return redirect('hangboard_detail', hangboard_id=hangboard.pk, username=username)
    else:
        context['form'] = AddHangboardForm(initial=initial_fields)
    return render(request, template_name=template_name, context=context)