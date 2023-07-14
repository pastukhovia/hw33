import pytest

from goals.models import BoardParticipant
from goals.serializers import GoalCategorySerializer
from tests.factories import GoalCategoryFactory, UserFactory


@pytest.mark.django_db
def test_unauthorized_access_to_goal_cat(client):
    response = client.get(path='/goals/goal_category/list')

    assert response.status_code == 403
    assert response.data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_authorized_access_to_goal_cat(client, user, user_login, create_password_and_login):
    create_password_and_login(user=user)
    response = client.get(path='/goals/goal_category/list')

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_owner_create_goal_cat(client, user, board, create_password_and_login):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    data = {
        'board': board.pk,
        'title': 'Test category'
    }

    response = client.post(
        path='/goals/goal_category/create',
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_reader_create_goal_cat(client, user, board, create_password_and_login):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )

    data = {
        'board': board.pk,
        'title': 'Test category'
    }

    response = client.post(
        path='/goals/goal_category/create',
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_writer_create_goal_cat(client, user, board, create_password_and_login):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.writer
    )

    data = {
        'board': board.pk,
        'title': 'Test category'
    }

    response = client.post(
        path='/goals/goal_category/create',
        data=data,
        content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_list_own_goal_cat(client, user, board, create_password_and_login):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )
    categories = GoalCategoryFactory.create_batch(size=5)

    for category in categories:
        category.board = board
        category.user = user
        category.save()

    expected_data = GoalCategorySerializer(categories, many=True).data
    # это нужно, потому что вью возвращает категории, отсортированные по названию, а сериализатор - по id
    expected_data = sorted(expected_data, key=lambda d: d['title'])

    response = client.get(path='/goals/goal_category/list')

    assert response.status_code == 200
    assert response.data == expected_data


@pytest.mark.django_db
def test_list_goal_cat_from_another_board(client, user, board, create_password_and_login, goal_category):
    '''
    Этот тест может иногда валиться из-за того, что фабрика рандомно создает несколько пользователей с одним именем
    '''
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )
    other_categories = GoalCategoryFactory.create_batch(size=5)

    not_expected_data = GoalCategorySerializer(other_categories, many=True).data
    # это нужно, потому что вью возвращает категории, отсортированные по названию, а сериализатор - по id
    not_expected_data = sorted(not_expected_data, key=lambda d: d['title'])

    response = client.get(path='/goals/goal_category/list')

    assert response.status_code == 200
    assert response.data == [GoalCategorySerializer(goal_category).data]
    assert not_expected_data not in response.data


@pytest.mark.django_db
def test_retrieve_own_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.get(path=f'/goals/goal_category/{goal_category.pk}')

    assert response.status_code == 200
    assert response.data == GoalCategorySerializer(goal_category).data


@pytest.mark.django_db
def test_retrieve_others_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )

    response = client.get(path=f'/goals/goal_category/{goal_category.pk}')

    assert response.status_code == 200
    assert response.data == GoalCategorySerializer(goal_category).data


@pytest.mark.django_db
def test_owner_update_own_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.put(
        path=f'/goals/goal_category/{goal_category.pk}',
        data={'title': 'New test title', 'board': board.pk},
        content_type="application/json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_owner_update_others_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    another_user = UserFactory.create()
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )
    BoardParticipant.objects.create(
        user=another_user, board=board, role=BoardParticipant.Role.writer
    )

    response = client.put(
        path=f'/goals/goal_category/{goal_category.pk}',
        data={'title': 'New test title', 'board': board.pk},
        content_type="application/json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_writer_update_own_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.writer
    )

    response = client.put(
        path=f'/goals/goal_category/{goal_category.pk}',
        data={'title': 'New test title', 'board': board.pk},
        content_type="application/json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_writer_update_others_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    another_user = UserFactory.create()
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.writer
    )
    BoardParticipant.objects.create(
        user=another_user, board=board, role=BoardParticipant.Role.writer
    )

    response = client.put(
        path=f'/goals/goal_category/{goal_category.pk}',
        data={'title': 'New test title', 'board': board.pk},
        content_type="application/json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_reader_update_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )

    response = client.put(
        path=f'/goals/goal_category/{goal_category.pk}',
        data={'title': 'New test title', 'board': board.pk},
        content_type="application/json"
    )

    assert response.status_code == 403


@pytest.mark.django_db
def test_owner_delete_own_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.delete(path=f'/goals/goal_category/{goal_category.pk}')

    assert response.status_code == 204


@pytest.mark.django_db
def test_owner_delete_others_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    another_user = UserFactory.create()
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )
    BoardParticipant.objects.create(
        user=another_user, board=board, role=BoardParticipant.Role.writer
    )

    response = client.delete(path=f'/goals/goal_category/{goal_category.pk}')

    assert response.status_code == 204


@pytest.mark.django_db
def test_writer_delete_own_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.writer
    )

    response = client.delete(path=f'/goals/goal_category/{goal_category.pk}')

    assert response.status_code == 204


@pytest.mark.django_db
def test_writer_delete_others_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    another_user = UserFactory.create()
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.writer
    )
    BoardParticipant.objects.create(
        user=another_user, board=board, role=BoardParticipant.Role.writer
    )

    response = client.delete(path=f'/goals/goal_category/{goal_category.pk}')

    assert response.status_code == 204


@pytest.mark.django_db
def test_reader_delete_goal_cat(client, user, board, create_password_and_login, goal_category):
    create_password_and_login(user=user)
    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.reader
    )

    response = client.delete(path=f'/goals/goal_category/{goal_category.pk}')

    assert response.status_code == 403
