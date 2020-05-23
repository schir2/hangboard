from django.shortcuts import render


def home_view(request):
    template_name = 'main/index.html'
    context = dict()
    context['title'] = 'Home'
    context['description'] = 'App for all things hangboarding'

    return render(request, context=context, template_name=template_name)


def login_view(request):
    template_name = 'main/login.html'
    context = dict()
    context['title'] = 'Login'
    context['description'] = 'Login'

    return render(request, context=context, template_name=template_name)
