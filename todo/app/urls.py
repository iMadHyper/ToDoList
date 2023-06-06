from django.urls import re_path

from . import views


app_name = 'app'
urlpatterns = [
    re_path(r'^add_folder/$', views.add_folder, name='add_folder'),
    re_path(r'^remove_folder/(?P<pk>[0-9]+)/$', views.delete_folder, name='remove_folder'),

    re_path(r'^add/$', views.add_task, name='add_task'),
    re_path(r"^remove/(?P<pk>[0-9]+)/$", views.delete_task , name="delete_task"),
    re_path(r"^complete/(?P<pk>[0-9]+)/$", views.complete_task , name="complete_task"),

    re_path(r"^completed/$", views.completed_tasks , name="completed_tasks"),
    re_path(r"^upcoming/$", views.upcoming_tasks , name="upcoming_tasks"),

    re_path(r'^', views.index, name='index'),
]