import secrets
import string

import pytest
from pytest_factoryboy import register

from .factories import UserFactory, BoardFactory, GoalCategoryFactory, GoalFactory

register(UserFactory)
register(BoardFactory)
register(GoalCategoryFactory)
register(GoalFactory)


@pytest.fixture
@pytest.mark.django_db
def user_login(client):
    def _method(username, password):
        response = client.post(path='/core/login',
                               data={"username": username, "password": password},
                               content_type="application/json")

        return response

    return _method


@pytest.fixture
def generate_password():
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(15))


@pytest.fixture
@pytest.mark.django_db
def create_password_and_login(client, generate_password):
    def _method(user):
        password = generate_password
        user.set_password(password)
        user.save()

        response = client.post(path='/core/login',
                               data={"username": user.username, "password": password},
                               content_type="application/json")

        return response

    return _method
