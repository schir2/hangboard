from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def profile_view(request, *args, **kwargs):
    template_name = 'climbers/profile.html'
    context = dict()
    context['title'] = 'Profile'
    context['description'] = 'User Profile'
    return render(request, template_name=template_name, context=context)


@login_required
def preferences_view(request, *args, **kwargs):
    template_name = 'climbers/preferences.html'
    context = dict()
    context['title'] = 'Preferences'
    context['description'] = 'User Preferences'
    return render(request, template_name=template_name, context=context)


@login_required
def measurements_view(request, *args, **kwargs):
    template_name = 'climbers/measurements.html'
    context = dict()
    context['title'] = 'Measurements'
    context['description'] = 'User Measurements'
    return render(request, template_name=template_name, context=context)