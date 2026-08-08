from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter
from rest_framework.viewsets import ModelViewSet

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)

from .permissions import (
    IsAdminOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    GenreSerializer,
    ReviewReadSerializer,
    ReviewWriteSerializer,
    TitleReadSerializer,
    TitleSerializer,
)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class TitleViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    queryset = (
        Title.objects
        .annotate(rating=Avg('reviews__score'))
        .select_related('category')
        .prefetch_related('genre')
    )

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.request.query_params

        category = params.get('category')
        genre = params.get('genre')
        year = params.get('year')
        name = params.get('name')

        if category:
            queryset = queryset.filter(category__slug=category)

        if genre:
            queryset = queryset.filter(genre__slug=genre)

        if year:
            queryset = queryset.filter(year=year)

        if name:
            queryset = queryset.filter(name__icontains=name)

        return queryset.distinct()


class ReviewViewSet(ModelViewSet):

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(title_id=title_id)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReviewReadSerializer
        return ReviewWriteSerializer

    def perform_create(self, serializer):
        title = get_object_or_404(
            Title,
            pk=self.kwargs['title_id'],
        )
        serializer.save(
            author=self.request.user,
            title=title,
        )


class CommentViewSet(ModelViewSet):

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(review_id=review_id)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CommentReadSerializer
        return CommentWriteSerializer

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            pk=self.kwargs['review_id'],
        )
        serializer.save(
            author=self.request.user,
            review=review,
        )
