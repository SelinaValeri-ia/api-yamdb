"""Классы прав доступа для вьюсетов users/categories/genres/titles/reviews."""
from rest_framework import permissions


class IsAdmin(permissions.BasePermission):
    """Доступ только администратору."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """Чтение всем, запись — только администратору."""

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user

        return bool(
            user
            and user.is_authenticated
            and (
                user.is_admin
                or getattr(user, 'is_superuser', False)
                or getattr(user, 'role', None) == 'admin'
            )
        )


class IsAuthorOrModeratorOrAdminOrReadOnly(permissions.BasePermission):
    """Чтение всем, запись — автору объекта, модератору или администратору."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user
            or request.user.is_moderator
            or request.user.is_admin
        )
