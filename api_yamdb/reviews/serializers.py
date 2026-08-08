"""Сериализаторы отзывов и комментариев."""
from rest_framework import serializers

from reviews.models import Review, Comment


class ReviewWriteSerializer(serializers.ModelSerializer):
    """Создание и изменение отзыва пользователя на произведение."""

    class Meta:
        model = Review
        fields = ('id', 'text', 'score')
        read_only_fields = ('id',)

    def validate(self, attrs):
        """Запрещает повторный отзыв того же автора на то же произведение."""
        if self.instance is None:
            request = self.context['request']
            title_id = self.context['view'].kwargs['title_id']
            if Review.objects.filter(
                title_id=title_id, author=request.user,
            ).exists():
                raise serializers.ValidationError(
                    'Вы уже оставляли отзыв на это произведение.'
                )
        return attrs


class ReviewReadSerializer(serializers.ModelSerializer):
    """Чтение отзыва с именем автора вместо его id."""

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
    """Создание и изменение комментария к отзыву."""

    class Meta:
        model = Comment
        fields = ('id', 'text')
        read_only_fields = ('id',)


class CommentReadSerializer(serializers.ModelSerializer):
    """Чтение комментария с именем автора вместо его id."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = (
            'id',
            'text',
            'author',
            'pub_date',
        )
