from abc import ABCMeta, abstractmethod
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.core import paginator
from django.utils.decorators import method_decorator
from django.views import View

from .forms import *
from main.models import Workout
from main.models import WorkoutSet


class BaseView(TemplateView, metaclass=ABCMeta):

    @abstractmethod
    def get(self, request, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, request, *args, **kwargs):
        pass

    def pagination(self, data, results_per_page: int = 20) -> paginator:
        pass


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


@method_decorator(login_required, 'dispatch')
class WorkoutDetailView(DetailView):
    model = Workout
    context_object_name = 'workout'


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
