from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .filters import GoalDateFilter
from .models import GoalCategory, Goal, Comment, Board, Status
from .permissions import BoardPermissions, CanEditCategory, CanCreateCategory, CanCreateComment, CanEditGoal, \
    CanCreateGoal, CanEditComment
from .serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    CommentCreateSerializer, CommentSerializer, BoardCreateSerializer, BoardSerializer, BoardListSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [IsAuthenticated, CanCreateCategory, ]


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated, ]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]
    filterset_fields = ['board']

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        ).select_related('user')


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, CanEditCategory, ]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            board__participants__user=self.request.user,
            is_deleted=False
        )

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated, CanCreateGoal, ]


class GoalListView(ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=Status.archived).select_related('user')


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, CanEditGoal, ]

    def get_queryset(self):
        return Goal.objects.filter(
            category__board__participants__user=self.request.user
        ).exclude(status=Status.archived)

    def perform_destroy(self, instance):
        instance.status = Status.archived
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = Comment
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, CanCreateComment, ]


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [IsAuthenticated, ]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering_fields = ['updated', 'created']
    ordering = ["created"]

    def get_queryset(self):
        return Comment.objects.filter(
            goal__category__board__participants__user=self.request.user,
            goal=self.request.query_params['goal']
        ).select_related('user')


class CommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, CanEditComment, ]

    def get_queryset(self):
        return Comment.objects.filter(
            goal__category__board__participants__user=self.request.user
        )


class BoardCreateView(CreateAPIView):
    model = Board
    serializer_class = BoardCreateSerializer
    permission_classes = [IsAuthenticated, ]


class BoardListView(ListAPIView):
    model = Board
    serializer_class = BoardListSerializer
    permission_classes = [IsAuthenticated, BoardPermissions, ]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter
    ]
    ordering = ["title"]

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)


class BoardView(RetrieveUpdateDestroyAPIView):
    model = Board
    permission_classes = [IsAuthenticated, BoardPermissions, ]
    serializer_class = BoardSerializer

    def get_queryset(self):
        # Обратите внимание на фильтрацию – она идет через participants
        return Board.objects.filter(participants__user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance: Board):
        # При удалении доски помечаем ее как is_deleted,
        # «удаляем» категории, обновляем статус целей
        with transaction.atomic():
            instance.is_deleted = True
            instance.save()
            instance.categories.update(is_deleted=True)
            Goal.objects.filter(category__board=instance).update(
                status=4
            )
        return instance
