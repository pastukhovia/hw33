import pytest

from goals.models import BoardParticipant
from goals.serializers import GoalSerializer
from tests.factories import UserFactory, GoalFactory


@pytest.mark.django_db
def test_unauthorized_access_to_goal(client):
    response = client.get(path='/goals/goal/list')

    assert response.status_code == 403
    assert response.data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_authorized_access_to_goal(client, user, user_login, create_password_and_login):
    create_password_and_login(user=user)
    response = client.get(path='/goals/goal/list')

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_owner_create_goal(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    data = {
        'user': user.pk,
        'title': 'Test goal',
        'category': goal_category.pk
    }

    response = client.post(
        path='/goals/goal/create',
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_reader_create_goal(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )

    data = {
        'user': user.pk,
        'title': 'Test goal',
        'category': goal_category.pk
    }

    response = client.post(
        path='/goals/goal/create',
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_writer_create_goal(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    data = {
        'user': user.pk,
        'title': 'Test goal',
        'category': goal_category.pk
    }

    response = client.post(
        path='/goals/goal/create',
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_list_own_goal(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )
    goals = GoalFactory.create_batch(size=5)

    for goal in goals:
        goal.category = goal_category
        goal.user = user
        goal.save()

    response = client.get(path='/goals/goal/list')

    assert response.status_code == 200
    assert response.data == GoalSerializer(goals, many=True).data


@pytest.mark.django_db
def test_list_goal_from_another_board(client, user, board, create_password_and_login, goal_category, goal):
    '''
    Этот тест может иногда валиться из-за того, что фабрика рандомно создает несколько пользователей с одним именем
    '''
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )
    other_goals = GoalFactory.create_batch(size=5)
    not_expected_data = GoalSerializer(other_goals, many=True).data

    goal.category = goal_category
    goal.save()

    response = client.get(path='/goals/goal/list')

    assert response.status_code == 200
    assert response.data == [GoalSerializer(goal).data]
    assert not_expected_data not in response.data


@pytest.mark.django_db
def test_retrieve_own_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.get(path=f'/goals/goal/{goal.pk}')

    assert response.status_code == 200
    assert response.data == GoalSerializer(goal).data


@pytest.mark.django_db
def test_retrieve_others_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )

    response = client.get(path=f'/goals/goal/{goal.pk}')

    assert response.status_code == 200
    assert response.data == GoalSerializer(goal).data


@pytest.mark.django_db
def test_owner_update_own_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.put(
        path=f'/goals/goal/{goal.pk}',
        data={'title': 'New test title', 'category': goal.category.pk},
        content_type="application/json"
    )
    print(response.data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_owner_update_others_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    another_user = UserFactory.create()
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )
    BoardParticipant.objects.create(
        user=another_user, board=board, role=BoardParticipant.Role.writer
    )

    goal.user = another_user
    goal.save()

    response = client.put(
        path=f'/goals/goal/{goal.pk}',
        data={'title': 'New test title', 'category': goal.category.pk},
        content_type="application/json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_writer_update_own_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.writer
    )

    response = client.put(
        path=f'/goals/goal/{goal.pk}',
        data={'title': 'New test title', 'category': goal.category.pk},
        content_type="application/json"
    )
    print(response.data)

    assert response.status_code == 200


@pytest.mark.django_db
def test_writer_update_others_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    another_user = UserFactory.create()
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.writer
    )
    BoardParticipant.objects.create(
        user=another_user, board=board, role=BoardParticipant.Role.writer
    )

    goal.user = another_user
    goal.save()

    response = client.put(
        path=f'/goals/goal/{goal.pk}',
        data={'title': 'New test title', 'category': goal.category.pk},
        content_type="application/json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_reader_update_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )

    response = client.put(
        path=f'/goals/goal/{goal.pk}',
        data={'title': 'New test title', 'category': goal.category.pk},
        content_type="application/json"
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_owner_delete_own_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.delete(path=f'/goals/goal/{goal.pk}')

    assert response.status_code == 204


@pytest.mark.django_db
def test_owner_delete_others_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    another_user = UserFactory.create()
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )
    BoardParticipant.objects.create(
        user=another_user, board=board, role=BoardParticipant.Role.writer
    )

    goal.user = another_user
    goal.save()

    response = client.delete(path=f'/goals/goal/{goal.pk}')

    assert response.status_code == 204


@pytest.mark.django_db
def test_writer_delete_own_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.delete(path=f'/goals/goal/{goal.pk}')

    assert response.status_code == 204



@pytest.mark.django_db
def test_writer_delete_others_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    another_user = UserFactory.create()
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )
    BoardParticipant.objects.create(
        user=another_user, board=board, role=BoardParticipant.Role.writer
    )

    goal.user = another_user
    goal.save()

    response = client.delete(path=f'/goals/goal/{goal.pk}')

    assert response.status_code == 204


@pytest.mark.django_db
def test_reader_delete_goal(client, user, board, create_password_and_login, goal):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )

    response = client.delete(path=f'/goals/goal/{goal.pk}')

    assert response.status_code == 403
