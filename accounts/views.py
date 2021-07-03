from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from .forms import LoginForm
from django.http import HttpResponse, request
from django.contrib.auth import login, authenticate


class Login(LoginView):
    """ Login Page """

    form_class = LoginForm
    template_name = 'login.html'


"""

def signup(request):
    return render(request, 'registration/signup.html')
"""

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('app:index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



        





class Logout(LoginRequiredMixin, LogoutView):
    """ Logout Page """

    template_name = 'login.html'


