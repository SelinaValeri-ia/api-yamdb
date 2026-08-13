"""Кастомная модель пользователя YaMDb."""
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


def validate_username_not_me(value):
    """Запрещает использовать 'me' в качестве username."""
    if value.lower() == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено.'
        )


class User(AbstractUser):
    """Пользователь с ролью (user/moderator/admin) и биографией."""

    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text=(
            'Обязательное поле. Не более 150 символов. Только буквы, '
            'цифры и символы @/./+/-/_.'
        ),
        validators=[UnicodeUsernameValidator(), validate_username_not_me],
        error_messages={
            'unique': 'Пользователь с таким username уже существует.',
        },
    )
    email = models.EmailField('email address', unique=True, max_length=254)
    role = models.CharField(
        'роль',
        max_length=20,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField('биография', blank=True)

    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR
