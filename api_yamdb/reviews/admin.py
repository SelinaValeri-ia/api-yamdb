from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('title',)
    search_fields = (
        'author__username',
        'title__name',
    )
    ordering = ('-pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('text',)
    ordering = ('-pub_date',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'category')
    list_filter = ('category', 'genre', 'year')
    search_fields = ('name', 'description')
    filter_horizontal = ('genre',)
