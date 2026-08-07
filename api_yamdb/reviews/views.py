from rest_framework.viewsets import ModelViewSet

from reviews.models import Review, Comment
from reviews.serializers import (
    ReviewReadSerializer,
    ReviewWriteSerializer,
    CommentReadSerializer,
    CommentWriteSerializer
)

# TODO:
# После merge permissions
# подключить IsAuthorModeratorAdminOrReadOnly

class ReviewViewSet(ModelViewSet):

    def get_queryset(self):

        title_id = self.kwargs['title_id']
        return Review.objects.filter(title_id=title_id)

    def get_serializer_class(self):

        if self.action in ['list', 'retrieve']:
            return ReviewReadSerializer
        return ReviewWriteSerializer

    def perform_create(self, serializer):

        serializer.save(
            author=self.request.user,
        )

# TODO:
# После merge ветки с Title добавить:
# serializer.save(author=self.request.user, title=title)

class CommentViewSet(ModelViewSet):

    def get_queryset(self):
    
            review_id = self.kwargs['review_id']
            return Comment.objects.filter(review_id=review_id)
    
    def get_serializer_class(self):
    
        if self.action in ['list', 'retrieve']:
            return CommentReadSerializer
        return CommentWriteSerializer
    
    def perform_create(self, serializer):
    
        serializer.save(
            author=self.request.user,
            ) # TODO:
# После merge добавить review=review
