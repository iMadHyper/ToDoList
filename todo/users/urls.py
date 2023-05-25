from django.urls import re_path, include
from . import views


app_name = 'users'
urlpatterns = [
    re_path(r'^login/', views.login_user, name='login'),
    re_path(r'^register/', views.register_user, name='signup'),
    re_path(r'^logout/', views.signout, name='logout'),
]