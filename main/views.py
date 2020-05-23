from django.shortcuts import render


def home_view(request):
    template_name = 'main/index.html'
    context = dict()
    context['title'] = 'Home'
    context['description'] = 'App for all things hangboarding'

    return render(request, context=context, template_name=template_name)