"""Модели произведений, категорий, жанров, отзывов и комментариев."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


def get_current_year():
    """Возвращает текущий"""
    return timezone.now().year


class Category(models.Model):
    """Категория произведения (например, «Фильмы»)."""

    name = models.CharField('Название', max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Жанр, которым может быть помечено произведение."""

    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение — фильм, книга или песня, к которому пишут отзывы."""

    name = models.CharField(max_length=256)
    year = models.PositiveSmallIntegerField(
        validators=[MaxValueValidator(get_current_year)],
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Отзыв пользователя на произведение с оценкой от 1 до 10."""

    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
        related_name='reviews',
    )
    score = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Оценка',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение',
        related_name='reviews',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title_review',
            )
        ]

    def __str__(self):
        return f'Отзыв от {self.author}: {self.text[:50]}'


class Comment(models.Model):
    """Комментарий пользователя к отзыву."""

    text = models.TextField(verbose_name='Текст комментария')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария',
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name='Комментарий к отзыву',
        related_name='comments',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return f'Комментарий от {self.author}: {self.text[:50]}'
