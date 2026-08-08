from rest_framework import serializers

from reviews.models import Review, Comment


class ReviewWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('id', 'text', 'score')
        read_only_fields = ('id',)

    def validate(self, attrs):
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
