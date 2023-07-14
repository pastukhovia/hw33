import pytest


@pytest.mark.django_db
def test_create_user(client):
    user_data = {
        "username": "test_user",
        "password": "123123asd",
        "password_repeat": "123123asd"
    }

    response = client.post(
        path='/core/signup',
        data=user_data,
        content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_passwords_dont_match(client):
    user_data = {
        "username": "test_user",
        "password": "123123asd",
        "password_repeat": "123123asd1"
    }

    response = client.post(
        path='/core/signup',
        data=user_data,
        content_type="application/json"
    )

    assert response.status_code == 400
    assert response.data == {"password": ["Passwords don't match"]}


@pytest.mark.django_db
def test_password_is_weak(client):
    user_data = {
        "username": "test_user",
        "password": "123456",
        "password_repeat": "123456"
    }

    response = client.post(
        path='/core/signup',
        data=user_data,
        content_type="application/json"
    )

    assert response.status_code == 400


@pytest.mark.django_db
def test_user_already_exists(client):
    user_data = {
        "username": "test_user",
        "password": "123123asd",
        "password_repeat": "123123asd"
    }

    client.post(
        path='/core/signup',
        data=user_data,
        content_type="application/json"
    )

    second_user_data = {
        "username": "test_user",
        "password": "123123asd",
        "password_repeat": "123123asd"
    }

    response = client.post(
        path='/core/signup',
        data=second_user_data,
        content_type="application/json"
    )

    assert response.status_code == 400
    assert response.data == {"username": ["A user with that username already exists."]}
