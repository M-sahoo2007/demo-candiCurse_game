from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'avatar')}),
        ('Game data', {'fields': ('total_score', 'highest_level')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'total_score', 'highest_level', 'is_staff')
    search_fields = ('username', 'email')
