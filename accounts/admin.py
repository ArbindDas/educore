# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# from .models import User


# @admin.register(User) # Register the User model inside Django Admin using CustomUserAdmin.
# class CustomUserAdmin(UserAdmin):   # CustomUserAdmin inherits everything from UserAdmin

#     list_display = (
#         "id",
#         "username",
#         "email",
#         "role",
#         "is_staff",
#         "is_superuser",
#         "date_joined",
#         "is_active",    
#         "last_login",
#     )

#     list_filter = (
#         "role",
#         "is_staff",
#         "is_superuser",
#     )

#     search_fields = (
#         "username",
#         "email",
#     )

#     ordering = ("id",)

#     fieldsets = UserAdmin.fieldsets + (
#         (
#             "Role Management",
#             {
#                 "fields": ("role",)
#             },
#         ),
#     )

#     add_fieldsets = (
#         (
#             None,
#             {
#                 "classes": ("wide",),
#                 "fields": (
#                     "username",
#                     "email",
#                     "password1",
#                     "password2",
#                     "role",
#                 ),
#             },
#         ),
#     )



from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin          # ← swap this in
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from .models import User


def user_count_badge(request):
    """Badge showing total user count in sidebar."""
    return str(User.objects.count())


@admin.register(User)
class CustomUserAdmin(ModelAdmin, UserAdmin):   # ModelAdmin first!

    # Unfold form overrides (for proper Tailwind styling)
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    # ---- Unfold extras ----
    list_fullwidth = True
    warn_unsaved_form = True
    compressed_fields = True

    list_display = (
        "id", "username", "email", "role",
        "is_staff", "is_superuser",
        "date_joined", "is_active", "last_login",
    )
    list_filter = ("role", "is_staff", "is_superuser", "is_active")
    search_fields = ("username", "email")
    ordering = ("id",)

    fieldsets = UserAdmin.fieldsets + (
        ("Role Management", {"fields": ("role",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "password1", "password2", "role"),
        }),
    )