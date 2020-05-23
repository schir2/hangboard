from django.urls import path
from django.urls import include

from main.views import home_view
from main.views import login_view

urlpatterns = [
    path('', home_view, name='home'),
    path('login', login_view, name='login'),
]