from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User) # Register the User model inside Django Admin using CustomUserAdmin.
class CustomUserAdmin(UserAdmin):   # CustomUserAdmin inherits everything from UserAdmin

    list_display = (
        "id",
        "username",
        "email",
        "role",
        "is_staff",
        "is_superuser",
        "date_joined",
        "is_active",    
        "last_login",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
    )

    ordering = ("id",)

    fieldsets = UserAdmin.fieldsets + (
        (
            "Role Management",
            {
                "fields": ("role",)
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "password1",
                    "password2",
                    "role",
                ),
            },
        ),
    )