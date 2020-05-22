from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request, *args, **kwargs):
    template_name = 'climbers/profile.html'
    context = dict()
    return render(request, template_name=template_name, context=context)