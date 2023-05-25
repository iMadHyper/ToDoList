from django.urls import re_path, include
from . import views


app_name = 'users'
urlpatterns = [
    re_path(r'^login/', views.LoginUser.as_view(), name='login'),
    re_path(r'^register/', views.RegisterUser.as_view(), name='signup'),
    re_path(r'^logout/', views.signout, name='logout'),
]