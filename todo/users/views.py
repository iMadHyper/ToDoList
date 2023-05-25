from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
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
    

# Log in
def login_user(request):
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:index')
        else:
            messages.success(request, 'Something\'s gone wrong')
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')
    

# Sign up
def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('app:index')
    else:
        form = RegisterUserForm()
        return render(request, 'users/register.html', {'form':form})


def signout(request):
    logout(request)
    return redirect('main:main')