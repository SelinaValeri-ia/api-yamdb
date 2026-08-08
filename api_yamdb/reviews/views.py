"""Вьюсеты отзывов и комментариев, вложенные в /titles/<title_id>/."""
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from api.permissions import IsAuthorOrModeratorOrAdminOrReadOnly
from reviews.models import Review, Title
from reviews.serializers import (
    ReviewReadSerializer,
    ReviewWriteSerializer,
    CommentReadSerializer,
    CommentWriteSerializer
)


class ReviewViewSet(ModelViewSet):
    """CRUD отзывов на конкретное произведение (без PUT)."""

    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options',
    ]

    def get_title(self):
        """Возвращает произведение из URL или 404."""
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def get_queryset(self):
        return self.get_title().reviews.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ReviewReadSerializer
        return ReviewWriteSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.get_title(),
        )


class CommentViewSet(ModelViewSet):
    """CRUD комментариев к конкретному отзыву (без PUT)."""

    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options',
    ]

    def get_review(self):
        """Возвращает отзыв из URL или 404."""
        return get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
            title_id=self.kwargs['title_id'],
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CommentReadSerializer
        return CommentWriteSerializer

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.get_review(),
        )
