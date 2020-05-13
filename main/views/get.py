from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from main.models import Workout
from main.models import WorkoutSet


@method_decorator(login_required, 'dispatch')
class WorkoutListView(ListView):
    model = Workout
    paginate_by = 20
    context_object_name = 'workouts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_queryset(self):
        return Workout.objects.filter(climber=self.request.user)


@login_required
def workout_detail_view(request, *args, **kwargs):
    template_name = 'main/workout_detail.html'
    context = dict()
    context['title'] = 'Workout Detail'
    context['workout'] = Workout.objects.get(slug=kwargs['slug'])

    if request.method == 'POST':
        pass
    else:
        pass

    return render(request, template_name=template_name, context=context)


@method_decorator(login_required, 'dispatch')
class WorkoutSetDetailView(View):
    template_name = 'main/workoutset_detail.html'

    def get(self, request, *args, **kwargs):
        context = dict()
        workout = Workout.objects.get(slug=self.kwargs['workout_slug'])
        context['workoutset'] = WorkoutSet.objects.filter(
            climber=self.request.user,
            workout=workout,
            position=self.kwargs['position'],
        )
        return render(request, template_name=self.template_name, context=context)


