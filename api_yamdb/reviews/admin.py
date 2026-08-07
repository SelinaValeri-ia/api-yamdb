from django.contrib import admin

from .models import Review, Comment


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'score', 'pub_date')
    list_filter = ('title',)
    search_fields = (
        'author__username',
        'title__name'
    )
    ordering = ('-pub_date',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'review', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('text',)
    ordering = ('-pub_date',)
