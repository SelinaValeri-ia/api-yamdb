"""Регистрация модели User в админке."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class YamdbUserAdmin(UserAdmin):
    """Админка пользователя с дополнительными полями role и bio."""

    list_display = UserAdmin.list_display + ('role', 'bio')
    fieldsets = UserAdmin.fieldsets + (
        ('YaMDb', {'fields': ('role', 'bio')}),
    )
