import pytest
from hr import settings
from rest_framework.test import APIClient

from hr.users.config import Config
from hr.users.tests.factories import UserFactory


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup):
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': ':memory:',
    }


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def user(db):
    return UserFactory(role=Config.HR)


@pytest.fixture
def auth_client(user, client):
    client.force_authenticate(user)
    return client
