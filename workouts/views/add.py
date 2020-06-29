from abc import abstractmethod
from abc import ABCMeta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.db.models import Q

from dal import autocomplete

from workouts.forms.add import AddWorkoutForm
from workouts.forms.add import AddWorkoutSetForm
from workouts.forms.add import AddHoldForm

from workouts.models import Workout
from workouts.models import WorkoutSet
from workouts.models import Exercise
from workouts.models import Hangboard
from workouts.models import HoldType
from workouts.models import Hold


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


class AddHangboardView(AddSimpleModelView):
    model = Hangboard


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


class AutoCompleteHoldView(autocomplete.Select2QuerySetView):
    model = Hold

    # TODO Implement filtering by hangboard and ordering

    def get_queryset(self):
        qs = self.model.objects.filter(Q(custom=False) | Q(climber=self.request.user))
        if self.q:
            qs = qs.filter(Q(name__istartswith=self.q))
        return qs

    def post(self, request, *args, **kwargs):
        # TODO Add proper redirect to add_hold
        return redirect('workout_list')


@login_required
def add_workout_view(request):
    template_name = 'workouts/add/workout.html'
    context = dict()
    context['title'] = 'Add Workout'
    if request.method == 'POST':
        context['form'] = AddWorkoutForm(request.POST)
        if context['form'].is_valid():
            workout = Workout.objects.add_workout(
                climber=request.user,
                **context['form'].cleaned_data,
            )
            return redirect('workouts:workout_detail', workout_id=workout.id)
    else:
        context['form'] = AddWorkoutForm()
    return render(request, template_name=template_name, context=context)


@login_required
def add_workout_set_view(request, workout_id, previous=None):
    template_name = 'workouts/add/workout_set.html'
    context = dict()
    context['title'] = 'Add Workout Set'
    workout = get_object_or_404(Workout, pk=workout_id)
    initial_fields = {'workout': workout_id, 'climber': request.user.pk, 'previous': previous, }
    if request.method == 'POST':
        context['form'] = AddWorkoutSetForm(request.POST, initial=initial_fields)
        previous = get_object_or_404(WorkoutSet, pk=previous) if previous else None
        if context['form'].is_valid():
            workout_set = WorkoutSet.objects.add_workout_set(
                climber=request.user,
                workout=workout,
                previous=previous,
                **context['form'].cleaned_data
            )
            workout_set.save()
            return redirect('workouts:workout_detail', workout_id=workout.pk)
    else:
        context['form'] = AddWorkoutSetForm(initial=initial_fields)

    return render(request, template_name=template_name, context=context)


@login_required
def add_hold_view(request, hangboard_id):
    template_name = 'workouts/add/hold.html'
    context = dict()
    context['title'] = 'Add Hold'
    initial_fields = {'hangboard': hangboard_id, 'climber': request.user.pk}
    if request.method == 'POST':
        context['form'] = AddHoldForm(request.POST, initial=initial_fields)
        if context['form'].is_valid():
            context['form'].save()
            initial_fields.update(context['form'].cleaned_data)
            initial_fields['position_id'] += 1
    context['form'] = AddHoldForm(initial=initial_fields)
    return render(request, template_name=template_name, context=context)
