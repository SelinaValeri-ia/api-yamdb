from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class YamdbUserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('role', 'bio')
    fieldsets = UserAdmin.fieldsets + (
        ('YaMDb', {'fields': ('role', 'bio')}),
    )
