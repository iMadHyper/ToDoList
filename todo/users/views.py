from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import LoginUserForm, RegisterUserForm
    

# Log in
def login_user(request):
    # Check to see if logging in
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('app:index')
        else:
            error = 'Username or password is incorrect!'
            return render(request, 'users/login.html', { 'error' : error })
    else:
        form = LoginUserForm()
        return render(request, 'users/login.html', { 'form' : form })
    

# Sign up
def signup_user(request):
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
            print(form.errors)
            messages.success(request, f'{form.errors}')
            return render(request, 'users/signup.html', {'form':form})
    else:
        form = RegisterUserForm()
        return render(request, 'users/signup.html', {'form':form})


def signout(request):
    logout(request)
    return redirect('main:main')