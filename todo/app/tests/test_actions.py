import pytest

from app import actions

from app import models

from datetime import date, timedelta


def test_get_overdue_tasks(create_user):
    '''Test if user's overdue task is in overdue tasks'''
    user = create_user(username='user1')
    task = models.Task.objects.create(
        user=user,
        name='task1',
        description='smth smth',
        date=date.today() - timedelta(days=1)
    )
    tasks = actions.get_overdue_tasks(user)
    assert task in tasks


def test_get_today_tasks(create_user):
    '''Test if user's today task is in today tasks'''
    user = create_user(username='user1')
    task = models.Task.objects.create(
        user=user,
        name='task1',
        description='smth smth'
    )
    tasks = actions.get_today_tasks(user)
    assert task in tasks


def test_get_upcoming_tasks(create_user):
    '''Test if user's upcoming task is in upcoming tasks'''
    user = create_user(username='user1')
    task = models.Task.objects.create(
        user=user,
        name='task1',
        description='smth smth',
        date=date.today() + timedelta(days=1)
    )
    tasks = actions.get_upcoming_tasks(user)
    assert task in tasks


def test_get_completed_tasks(create_user):
    '''
    Test if user's completed task is in completed tasks and
    not completed is not
    '''
    user = create_user(username='user1')
    task = models.Task.objects.create(
        user=user,
        name='task1',
        description='smth smth',
        date=date.today() + timedelta(days=1),
        is_completed=False
    )
    task2 = models.Task.objects.create(
        user=user,
        name='task1',
        description='smth smth',
        date=date.today() + timedelta(days=1),
        is_completed=True
    )
    tasks = actions.get_completed_tasks(user)
    assert task not in tasks
    assert task2 in tasks


def test_get_folder(create_user):
    '''User have 2 folders'''
    user = create_user(username='user1')
    folder1 = models.Folder.objects.create(user=user, name='folder1')
    folder2 = models.Folder.objects.create(user=user, name='folder2')
    assert user.folders.count() == 2


def test_get_folder2(create_user):
    '''Each user have 1 folder'''
    user1 = create_user(username='user1')
    user2 = create_user(username='user2')
    folder1 = models.Folder.objects.create(user=user1, name='folder1')
    folder2 = models.Folder.objects.create(user=user2, name='folder2')
    assert user1.folders.count() == 1
    assert user2.folders.count() == 1


def test_get_folder_tasks(auto_login_user, create_user):
    user1 = create_user(username='user1')
    folder1 = models.Folder.objects.create(user=user1, name='folder1')
    folder2 = models.Folder.objects.create(user=user1, name='folder2')
    task1 = models.Task.objects.create(
        user=user1,
        folder=folder1,
        name='task1',
        description='smth smth'
    )
    task2 = models.Task.objects.create(
        user=user1,
        folder=folder2,
        name='task1',
        description='smth smth'
    )

    assert folder1.tasks.count() == 1
    assert folder2.tasks.count() == 1

    assert task1 in folder1.get_tasks()
    assert task2 in folder2.get_tasks()