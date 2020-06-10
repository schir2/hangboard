from abc import abstractmethod
from abc import ABCMeta

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.db.models import Q

from dal import autocomplete

from workouts.forms.add import AddWorkoutForm
from workouts.forms.add import AddWorkoutSetForm

from workouts.models import Workout
from workouts.models import WorkoutSet
from workouts.models import Exercise
from workouts.models import Hangboard
from workouts.models import HoldType


class AddSimpleModelView(LoginRequiredMixin, CreateView, metaclass=ABCMeta):
    @property
    @abstractmethod
    def model(self):
        pass

    template_name = 'workouts/add/simple_model.html'
    fields = ('name',)

    def form_valid(self, form):
        form.instance.climber = self.request.user
        return super().form_valid(form)


class AutoCompleteSimpleView(autocomplete.Select2QuerySetView, metaclass=ABCMeta):

    @property
    @abstractmethod
    def model(self):
        pass

    def get_queryset(self):
        qs = self.model.objects.filter(Q(custom=False) | Q(climber=self.request.user))
        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q))
        return qs


class AutoCompleteExerciseView(AutoCompleteSimpleView):
    model = Exercise


class AutoCompleteHoldTypeView(AutoCompleteSimpleView):
    model = HoldType


class AutoCompleteHangboardView(AutoCompleteSimpleView):
    model = Hangboard


class AutoCompleteLeftHold(autocomplete.Select2QuerySetView):
    # TODO Implement filtering by hangboard and ordering
    def get_queryset(self):
        qs = self.model.objects.filter(Q(custom=False) | Q(climber=self.request.user))
        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q))
        return qs


class AutoCompleteRightHold(autocomplete.Select2QuerySetView):
    # TODO Implement filtering by hangboard and ordering
    def get_queryset(self):
        qs = self.model.objects.filter(Q(custom=False) | Q(climber=self.request.user))
        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q))
        return qs


@login_required
def add_workout_view(request):
    template_name = 'workouts/add/workout.html'
    context = dict()
    context['title'] = 'Add Workout'
    if request.method == 'POST':
        context['form'] = AddWorkoutForm(request.POST)
        if context['form'].is_valid():
            workout = Workout.objects.add_workout(climber=request.user, **context['form'].cleaned_data)
            return redirect('workout_detail', workout_id=workout.id)
        else:
            raise ValueError('Invalid Form Values')
    else:
        context['form'] = AddWorkoutForm()
    return render(request, template_name=template_name, context=context)


@login_required
def add_workout_set_view(request, workout_id, previous=None):
    template_name = 'workouts/add/workout_set.html'
    context = dict()
    context['title'] = 'Add Workout Set'
    workout = Workout.objects.get(pk=workout_id)
    initial_fields = {'workout': workout_id, 'climber': request.user.pk, 'previous': previous, }
    if request.method == 'POST':
        context['form'] = AddWorkoutSetForm(request.POST, initial=initial_fields)
        previous = WorkoutSet.objects.get(pk=previous) if previous else None
        if context['form'].is_valid():
            workout_set = WorkoutSet.objects.add_workout_set(climber=request.user, workout=workout, previous=previous,
                **context['form'].cleaned_data)
            workout_set.save()
            return redirect('workout_detail', workout_id=workout.pk)
        else:
            raise ValueError('Invalid Form Values')
    else:
        context['form'] = AddWorkoutSetForm(initial=initial_fields)

    return render(request, template_name=template_name, context=context)
