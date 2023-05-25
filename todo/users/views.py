from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .forms import LoginUserForm, RegisterUserForm

from django.views import generic

# Регистрация
class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('app:index')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('app:index')


# Авторизация
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse_lazy('app:index')


def signout(request):
    logout(request)
    return redirect('main:main')