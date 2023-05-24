from django.urls import re_path, include
from . import views


app_name = 'users'
urlpatterns = [
    re_path(r'^login/', views.login, name='login'),
    re_path(r'^register/', views.login, name='signup'),
    re_path(r'^', include('main.urls')),
]