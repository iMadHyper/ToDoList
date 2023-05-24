from django.shortcuts import render, redirect

from django.contrib.auth import authenticate,login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def login(request):
    if request.user.is_authenticated:
        return redirect('todo/main.html')
     
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username =username, password = password)
 
        if user is not None:
            login(request,user)
            return redirect('todo/main.html')
        else:
            form = AuthenticationForm()
            return render(request,'users/login.html',{'form':form})
     
    else:
        form = AuthenticationForm()
        return render(request, 'users/login.html', {'form':form})


def register(request):
    if request.user.is_authenticated:
        return redirect('todo/main.html')
     
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
 
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username,password = password)
            login(request, user)
            return redirect('/books')
         
        else:
            return render(request,'users/register.html',{'form':form})
     
    else:
        form = UserCreationForm()
        return render(request,'users/register.html',{'form':form})