from django.views.generic.list import ListView
from django.views import View
from django.shortcuts import render

from workouts.models import Workout
from workouts.models import WorkoutSet
from workouts.models import Exercise
from workouts.models import Hangboard


class BaseListView(ListView):
    paginate_by = 20

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return self.model.objects.filter(climber=self.request.user)


class WorkoutListView(BaseListView):
    model = Workout
    context_object_name = 'workouts'
    template_name = 'workouts/get/workout_list.html'


class ExerciseListView(BaseListView):
    model = Exercise
    context_object_name = 'exercises'
    template_name = 'workouts/get/exercise_list.html'


class HangboardListView(BaseListView):
    model = Hangboard
    context_object_name = 'hangboards'
    template_name = 'workouts/get/hangboard_list.html'


def workout_detail_view(request, workout_id, *args, **kwargs):
    template_name = 'workouts/get/workout_detail.html'
    context = dict()
    context['title'] = 'Workout Detail'
    context['workout'] = Workout.objects.get(pk=workout_id)

    return render(request, template_name=template_name, context=context)


def hangboard_detail_view(request, hangboard_id, *args, **kwargs):
    template_name = 'workouts/get/hangboard_detail.html'
    context= dict()
    context['title'] = 'Hangboard Detail'
    context['hangboard'] = Hangboard.objects.get(pk=hangboard_id)

    return render(request, template_name=template_name, context=context)


class WorkoutSetDetailView(View):
    template_name = 'workouts/get/workoutset_detail.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        workout = Workout.objects.get(slug=self.kwargs['workout_slug'])
        context['workoutset'] = WorkoutSet.objects.filter(
            climber=self.request.user,
            workout=workout,
            position=self.kwargs['position'],
        )
        return render(request, template_name=self.template_name, context=context)


