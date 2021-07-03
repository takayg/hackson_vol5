from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.http import HttpResponse, request


class Login(LoginView):
    """ Login Page """

    form_class = LoginForm
    template_name = 'login.html'


def signup(request):
    return render(request, 'registration/signup.html')
        





class Logout(LoginRequiredMixin, LogoutView):
    """ Logout Page """

    template_name = 'login.html'


