from django.shortcuts import render, redirect, HttpResponse


def main(request):
    if request.user.is_authenticated:
        return render(request, 'todo/main.html')
    else:
        return render(request, 'main/main.html')