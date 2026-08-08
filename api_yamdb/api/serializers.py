from datetime import date

from rest_framework import serializers

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
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
        fields = ('text', 'score')


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
        fields = ('text',)


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
