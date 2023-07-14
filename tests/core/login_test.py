import pytest


@pytest.mark.django_db
def test_login(client, user, generate_password):
    password = generate_password
    user.set_password(password)
    user.save()

    expected_data = {
        'id': user.pk,
        'username': str(user.username),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }

    response = client.post(
        path='/core/login',
        data={'username': user.username, 'password': password},
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.json() == expected_data


@pytest.mark.django_db
def test_wrong_credentials(client, user, generate_password):
    password = generate_password
    user.set_password(password)
    user.save()

    response = client.post(
        path='/core/login',
        data={'username': user.username, 'password': password + '1'},
        content_type="application/json"
    )

    assert response.status_code == 400
    assert response.json() == {"response": ["Wrong credentials"]}
