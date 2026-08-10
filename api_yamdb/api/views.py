"""Вьюхи аутентификации и вьюсеты users/categories/genres/titles."""
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404

from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from users.models import User

from .permissions import (
    IsAdmin,
    IsAdminOrReadOnly,
    IsAuthorOrModeratorOrAdminOrReadOnly,
)
from .serializers import (
    CategorySerializer,
    CommentReadSerializer,
    CommentWriteSerializer,
    GenreSerializer,
    ReviewReadSerializer,
    ReviewWriteSerializer,
    SignUpSerializer,
    TitleReadSerializer,
    TitleSerializer,
    TokenSerializer,
    UserMeSerializer,
    UserSerializer,
)


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрирует пользователя и отправляет код подтверждения на email."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    email = serializer.validated_data['email']
    username = serializer.validated_data['username']

    user, _ = User.objects.get_or_create(username=username, email=email)
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Код подтверждения для YaMDb',
        message=f'Ваш код подтверждения: {confirmation_code}',
        from_email=None,
        recipient_list=[user.email],
    )

    return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def token_obtain(request):
    """Выдаёт JWT-токен по username и коду подтверждения."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']

    user = get_object_or_404(User, username=username)
    if not default_token_generator.check_token(user, confirmation_code):
        return Response(
            {'confirmation_code': 'Неверный код подтверждения.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    token = AccessToken.for_user(user)
    return Response({'token': str(token)}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """CRUD пользователей администратором + self-service /users/me/."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    lookup_field = 'username'
    search_fields = ('username',)
    http_method_names = [
        'get', 'post', 'patch', 'delete', 'head', 'options',
    ]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(IsAuthenticated,),
        url_path='me',
    )
    def me(self, request):
        """Возвращает или обновляет профиль текущего пользователя."""
        if request.method == 'PATCH':
            serializer = UserMeSerializer(
                request.user, data=request.data, partial=True,
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        serializer = UserMeSerializer(request.user)
        return Response(serializer.data)


class CategoryViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Список, создание и удаление категорий (без detail-эндпоинта)."""

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
    """Список, создание и удаление жанров (без detail-эндпоинта)."""

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
    """CRUD произведений с рейтингом и фильтрами (без PUT)."""

    queryset = (
        Title.objects
        .annotate(rating=Avg('reviews__score'))
        .select_related('category')
        .prefetch_related('genre')
        .order_by('id')
    )

    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name',)
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete',
        'head',
        'options',
    ]

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleSerializer

    def get_queryset(self):
        """Фильтрует по category/genre/year/name из query-параметров."""
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
    """Работа с отзывами на конкретное произведение."""

    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs['title_id']
        return Review.objects.filter(
            title_id=title_id
        ).select_related('author')

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
    """Работа с комментариями конкретного отзыва."""

    permission_classes = (IsAuthorOrModeratorOrAdminOrReadOnly,)

    def get_queryset(self):
        review_id = self.kwargs['review_id']
        return Comment.objects.filter(
            review_id=review_id
        ).select_related('author')

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
