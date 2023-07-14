import pytest


@pytest.mark.django_db
def test_unauthorized_access_to_profile(client):
    response = client.get(
        path='/core/profile'
    )

    assert response.status_code == 403
    assert response.data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_authorized_access_to_profile(client, user, create_password_and_login):
    expected_data = {
        'id': user.pk,
        'username': str(user.username),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }

    create_password_and_login(user=user)

    response = client.get(
        path='/core/profile'
    )

    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_logout(client, user, create_password_and_login):
    create_password_and_login(user=user)

    client.delete(path='/core/profile')
    response = client.get(path='/core/profile')

    assert response.status_code == 403
    assert response.data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_change_password(client, user, user_login, generate_password):
    password = generate_password
    user.set_password(password)
    user.save()

    user_login(username=user.username, password=password)

    response = client.put(
        path='/core/update_password',
        data={'old_password': password, 'new_password': generate_password + '1'},
        content_type="application/json"
    )

    assert response.status_code == 200
    assert response.data == {'old_password': password, 'new_password': generate_password + '1'}


@pytest.mark.django_db
def test_old_password_doesnt_match(client, user, user_login, generate_password):
    password = generate_password
    user.set_password(password)
    user.save()

    user_login(username=user.username, password=password)

    response = client.put(
        path='/core/update_password',
        data={'old_password': password + '1', 'new_password': generate_password + '1'},
        content_type="application/json"
    )

    assert response.status_code == 400
    assert response.data == {"old_password": ["Old password doesn't match"]}


@pytest.mark.django_db
def test_new_password_is_weak(client, user, user_login, generate_password):
    password = generate_password
    user.set_password(password)
    user.save()

    user_login(username=user.username, password=password)

    response = client.put(
        path='/core/update_password',
        data={'old_password': password, 'new_password': '123'},
        content_type="application/json"
    )

    assert response.status_code == 400
