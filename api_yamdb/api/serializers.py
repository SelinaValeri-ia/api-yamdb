"""Сериализаторы регистрации, токена, пользователей и произведений."""
from datetime import date

from rest_framework import serializers

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from users.models import User


class SignUpSerializer(serializers.Serializer):
    """Самостоятельная регистрация по email и username."""

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=User._meta.get_field('username').validators,
    )

    def validate(self, attrs):
        """Запрещает регистрацию с email/username другого пользователя."""
        email = attrs['email']
        username = attrs['username']
        user_by_email = User.objects.filter(email=email).first()
        user_by_username = User.objects.filter(username=username).first()

        if user_by_email and user_by_email.username != username:
            raise serializers.ValidationError({
                'email': (
                    'Пользователь с таким email уже зарегистрирован '
                    'под другим username.'
                ),
            })

        if user_by_username and user_by_username.email != email:
            raise serializers.ValidationError({
                'username': (
                    'Пользователь с таким username уже зарегистрирован '
                    'с другим email.'
                ),
            })

        return attrs


class TokenSerializer(serializers.Serializer):
    """Обмен username и кода подтверждения на JWT-токен."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    """Полный набор полей пользователя для администратора."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )


class UserMeSerializer(serializers.ModelSerializer):
    """Профиль пользователя для self-service /users/me/ (роль read-only)."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        )
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Категория произведения."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Жанр произведения."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    """Произведение для чтения: вложенные category/genre и рейтинг."""

    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'rating',
            'description',
            'genre',
            'category',
        )


class TitleSerializer(serializers.ModelSerializer):
    """Произведение для создания/изменения: category/genre по slug."""

    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(),
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        read_only_fields = ('id',)

    def validate_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего года.'
            )
        return value


class ReviewWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'text', 'score')
        read_only_fields = ('id',)

    def validate(self, attrs):
        if self.instance is not None:
            return attrs

        request = self.context['request']
        title_id = self.context['view'].kwargs['title_id']

        if Review.objects.filter(
            author=request.user,
            title_id=title_id
        ).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )

        return attrs


class ReviewReadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = (
            'id',
            'text',
            'author',
            'score',
            'pub_date',
        )


class CommentWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text')
        read_only_fields = ('id',)


class CommentReadSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
