from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework import serializers

from users.models import User


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(
        max_length=150,
        validators=[UnicodeUsernameValidator()],
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Использовать имя "me" в качестве username запрещено.'
            )
        return value

    def validate(self, attrs):
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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role',
        )
        read_only_fields = ('role',)
