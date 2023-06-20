import pytest

from django import urls


@pytest.mark.parametrize('view_name', ['users:login', 'users:signup'])
def test_auth_views_are_available(client, view_name):
    '''Auth pages are available to a non authenticated user'''
    url = urls.reverse(view_name)
    resp = client.get(url)
    assert resp.status_code == 200