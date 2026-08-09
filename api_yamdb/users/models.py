"""Кастомная модель пользователя YaMDb."""
from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLE_CHOICES = (
    (USER, 'Пользователь'),
    (MODERATOR, 'Модератор'),
    (ADMIN, 'Администратор'),
)


class User(AbstractUser):
    """Пользователь с ролью (user/moderator/admin) и биографией."""

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

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    def __str__(self):
        return self.username
