from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from main.forms import WorkoutSetForm
from main.models import Workout


# Create your views here.
@login_required
def workout_set_form_view(request):
    template_name = 'main/forms/workout_set.html'
    context = dict()
    context['title'] = 'Workout Set Form'
    if request.method == 'POST':
        form = WorkoutSetForm(request.user, request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        context['form'] = WorkoutSetForm(request.user)

    return render(request, template_name=template_name, context=context)
