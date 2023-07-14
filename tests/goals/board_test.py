import pytest

from goals.models import BoardParticipant
from goals.serializers import BoardListSerializer, BoardSerializer
from tests.factories import BoardFactory, UserFactory


@pytest.mark.django_db
def test_unauthorized_access_to_boards(client):
    response = client.get(path='/goals/board/list')

    assert response.status_code == 403
    assert response.data == {"detail": "Authentication credentials were not provided."}


@pytest.mark.django_db
def test_authorized_access_to_boards(client, user, user_login, create_password_and_login):
    create_password_and_login(user=user)
    response = client.get(path='/goals/board/list')

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_create_board(client, user, create_password_and_login):
    create_password_and_login(user=user)

    response = client.post(
        path='/goals/board/create',
        data={'title': 'Test board name'},
        content_type="application/json"
    )

    assert response.status_code == 201


@pytest.mark.django_db
def test_list_boards(client, user, create_password_and_login):
    create_password_and_login(user=user)

    boards = BoardFactory.create_batch(size=4)

    BoardParticipant.objects.create(
        user=user, board=boards[0], role=BoardParticipant.Role.owner
    )

    BoardParticipant.objects.create(
        user=user, board=boards[1], role=BoardParticipant.Role.writer
    )

    BoardParticipant.objects.create(
        user=user, board=boards[2], role=BoardParticipant.Role.reader
    )

    expected_data = BoardListSerializer([boards[0], boards[1], boards[2]], many=True).data
    # это нужно, потому что вью возвращает доски, отсортированные по названию, а сериализатор - по id
    expected_data = sorted(expected_data, key=lambda d: d['title'])

    response = client.get(path='/goals/board/list')

    assert response.status_code == 200
    assert response.data == expected_data
    assert BoardListSerializer(boards[3]).data not in response.data


@pytest.mark.django_db
def test_retrieve_board(client, user, board, create_password_and_login):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.get(path=f'/goals/board/{board.pk}')

    assert response.status_code == 200
    assert response.data == BoardSerializer(board).data


@pytest.mark.django_db
def test_add_new_participant(client, board, create_password_and_login):
    users = UserFactory.create_batch(size=2)
    create_password_and_login(user=users[0])

    new_participant = {'role': BoardParticipant.Role.reader, 'user': users[1].username}

    BoardParticipant.objects.create(
        user=users[0], board=board, role=BoardParticipant.Role.owner
    )

    response = client.put(
        path=f'/goals/board/{board.pk}',
        data={'participants': [new_participant], 'title': board.title},
        content_type="application/json"
    )

    assert response.status_code == 200


@pytest.mark.django_db
def test_change_title(client, board, user, create_password_and_login):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.put(
        path=f'/goals/board/{board.pk}',
        data={'participants': [], 'title': board.title + '1'},
        content_type="application/json"
    )
    print(board.title)
    print(response.data)

    assert response.status_code == 200
    assert response.data['title'] == board.title + '1'


@pytest.mark.django_db
def test_delete_board(client, board, user, create_password_and_login):
    create_password_and_login(user=user)

    BoardParticipant.objects.create(
        user=user, board=board, role=BoardParticipant.Role.owner
    )

    response = client.delete(path=f'/goals/board/{board.pk}')

    assert response.status_code == 204
