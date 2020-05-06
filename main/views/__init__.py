from abc import ABCMeta, abstractmethod
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core import paginator
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .forms import *
from main.models import Hangboard
from main.models import Workout


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