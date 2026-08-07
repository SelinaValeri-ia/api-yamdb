from rest_framework import serializers

from reviews.models import Review, Comment


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
        fields = ('text', )


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
