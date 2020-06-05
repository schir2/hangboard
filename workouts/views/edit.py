from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from workouts.forms.edit import EditExerciseForm


@login_required
def edit_exercise_view(request, exercise_id):
    template_name = 'workouts/add/exercise.html'
    context = dict()
    context['title'] = 'Edit Exercise'
    initial_fields = {'climber': request.user.pk, 'id':exercise_id}

    if request.method == 'POST':
        context['form'] = EditExerciseForm(request.POST)
        if context['form'].is_valid():
            context['form'].save()
        return redirect('exercise_list')
    else:
        context['form'] = EditExerciseForm(initial=initial_fields)
    return render(request, template_name=template_name, context=context)