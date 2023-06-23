from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .filters import GoalDateFilter
from .models import GoalCategory, Goal, Comment
from .permissions import IsOwner
from .serializers import GoalCategoryCreateSerializer, GoalCategorySerializer, GoalCreateSerializer, GoalSerializer, \
    CommentCreateSerializer, CommentSerializer


class GoalCategoryCreateView(CreateAPIView):
    model = GoalCategory
    serializer_class = GoalCategoryCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]


class GoalCategoryListView(ListAPIView):
    model = GoalCategory
    permission_classes = [IsAuthenticated, IsOwner, ]
    serializer_class = GoalCategorySerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    ordering_fields = ["title", "created"]
    ordering = ["title"]
    search_fields = ["title"]

    def get_queryset(self):
        return GoalCategory.objects.filter(
            user=self.request.user, is_deleted=False
        )


class GoalCategoryView(RetrieveUpdateDestroyAPIView):
    model = GoalCategory
    serializer_class = GoalCategorySerializer
    permission_classes = [IsAuthenticated, IsOwner, ]

    def get_queryset(self):
        return GoalCategory.objects.filter(user=self.request.user, is_deleted=False)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()
        return instance


class GoalCreateView(CreateAPIView):
    model = Goal
    serializer_class = GoalCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]


class GoalListView(ListAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]
    pagination_class = LimitOffsetPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = GoalDateFilter

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).exclude(status=4)


class GoalView(RetrieveUpdateDestroyAPIView):
    model = Goal
    serializer_class = GoalSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).exclude(status=4)

    def perform_destroy(self, instance):
        instance.status = 4
        instance.save()
        return instance


class CommentCreateView(CreateAPIView):
    model = Comment
    serializer_class = CommentCreateSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]


class CommentListView(ListAPIView):
    model = Comment
    permission_classes = [IsAuthenticated, IsOwner, ]
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination
    ordering_fields = ['updated', 'created']
    ordering = ["created"]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user, goal=self.request.query_params['goal'])


class CommentView(RetrieveUpdateDestroyAPIView):
    model = Comment
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwner, ]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
