from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from reviews.models import Category, Genre, Title

from .permissions import IsAdminOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    TitleReadSerializer,
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
