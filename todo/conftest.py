import pytest


@pytest.fixture
def create_user(django_user_model):
    def make_user(**kwargs):
        kwargs['password'] = 'password123'
        if 'username' not in kwargs:
            kwargs['username'] = 'username123'
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def auto_login_user(client, django_user_model):
    def make_auto_login(user=None):
        if user is None:
            user = django_user_model.objects.create(
                username='someone', password='password123'
            )
        client.login(username='someone', password='password123')
        return client, user
    return make_auto_login