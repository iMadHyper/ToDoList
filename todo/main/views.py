from django.shortcuts import render, redirect, HttpResponse


def main(request):
    if request.user.is_authenticated:
        return redirect('app:index')
    else:
        return render(request, 'main/main.html')