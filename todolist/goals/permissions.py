from rest_framework import permissions
from .models import BoardParticipant


class CanCreateCategory(permissions.BasePermission):
    message = 'Readers cannot create category'

    def has_permission(self, request, view):
        return BoardParticipant.objects.filter(
            user=request.user, board=request.data['board'], role=BoardParticipant.Role.owner
        ).exists() | BoardParticipant.objects.filter(
            user=request.user, board=request.data['board'], role=BoardParticipant.Role.writer
        ).exists()


class BoardPermissions(permissions.BasePermission):
    message = 'Only owners of boards can edit it'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj
            ).exists()
        return BoardParticipant.objects.filter(
            user=request.user, board=obj, role=BoardParticipant.Role.owner
        ).exists()


class CanEditCategory(permissions.BasePermission):
    message = 'Readers cannot edit categories'

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board=obj.board
            ).exists()

        return BoardParticipant.objects.filter(
            user=request.user, board=obj.board, role=BoardParticipant.Role.owner
        ).exists() | BoardParticipant.objects.filter(
            user=request.user, board=obj.board, role=BoardParticipant.Role.writer
        ).exists()


class CanCreateGoal(permissions.BasePermission):
    def has_permission(self, request, view):
        return BoardParticipant.objects.filter(
            user=request.user, board__categories=request.data['category'], role=BoardParticipant.Role.owner
        ).exists() | BoardParticipant.objects.filter(
            user=request.user, board__categories=request.data['category'], role=BoardParticipant.Role.writer
        ).exists()


class CanEditGoal(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
            user=request.user, board__categories=obj.category
            ).exists()

        return BoardParticipant.objects.filter(
            user=request.user, board__categories=obj.category, role=BoardParticipant.Role.owner
        ).exists() | BoardParticipant.objects.filter(
            user=request.user, board__categories=obj.category, role=BoardParticipant.Role.writer
        ).exists()


class CanCreateComment(permissions.BasePermission):
    def has_permission(self, request, view):
        return BoardParticipant.objects.filter(
            user=request.user, board__categories__goal=request.data['goal'], role=BoardParticipant.Role.owner
        ).exists() | BoardParticipant.objects.filter(
            user=request.user, board__categories__goal=request.data['goal'], role=BoardParticipant.Role.writer
        ).exists()


class CanEditComment(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return BoardParticipant.objects.filter(
                user=request.user, board__categories__goal=obj.goal
            ).exists()

        return BoardParticipant.objects.filter(
            user=request.user, board__categories__goal=obj.goal, role=BoardParticipant.Role.owner
        ).exists() | BoardParticipant.objects.filter(
            user=request.user, board__categories__goal=obj.goal, role=BoardParticipant.Role.writer
        ).exists()
