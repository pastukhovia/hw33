import factory

from core.models import User
from goals.models import Board, GoalCategory, Goal


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker('random_int')
    email = factory.Faker('email')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class BoardFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Board

    title = factory.Faker('word')


class GoalCategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = GoalCategory

    title = factory.Faker('word')
    user = factory.SubFactory(UserFactory)
    board = factory.SubFactory(BoardFactory)


class GoalFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Goal

    title = factory.Faker('word')
    user = factory.SubFactory(UserFactory)
    category = factory.SubFactory(GoalCategoryFactory)
