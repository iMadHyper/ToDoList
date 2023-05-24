from django.shortcuts import render, HttpResponse


def main(request):
    if request.user.is_authenticated:
        return HttpResponse('<h1>You are authenticated</h1')
    else:
        return render(request, 'main/main.html')