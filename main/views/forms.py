from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from main.forms import WorkoutSetForm


# Create your views here.
@login_required
def workout_set_form_view(request):
    template_name = 'main/forms/workout_set.html'
    context = dict()
    context['title'] = 'Workout Set Form'
    context['form'] = WorkoutSetForm(climber=request.user)

    return render(request, template_name=template_name, context=context)
