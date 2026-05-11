# from django.contrib import admin

# # Register your models here.



# from .models import (
#     PrincipalProfile,
#     TeacherProfile,
#     StudentProfile
# )


# @admin.register(PrincipalProfile)
# class PrincipalProfileAdmin(admin.ModelAdmin):
#     list_display = (
#         "id",
#         "phone_number",
#         "admin_level",
#         "office_room",
#         "designation",
#         "user_id"
#     )
    
#     search_fields = (
#         "user_username",
#         "phone_number",
#         "designation"
#     )
    
#     ordering = ("id",)
    

# @admin.register(TeacherProfile)
# class TeacherProfileAdmin(admin.ModelAdmin):
    
#     list_display = (
#         "id",
#         "phone_number",
#         "experience",
#         "qualification",
#         "joining_date",
#         "user_id"
#     )
    
    
#     search_fields = (
#         "user_username",
#         "qualification",
#     )
    
#     list_filter = (
#         "qualification",
#         "joining_date",
#     )
    
#     ordering = ("id",)
    

# @admin.register(StudentProfile)
# class StudentProfileAdmin(admin.ModelAdmin):
    
#     list_display = (
#         "id",
#         "roll_number",
#         "admission_number",
#         "address",
#         "user_id",
#         "academic_class_id"
#     )
    
#     list_filter = (
#         "academic_class",
#     )

#     ordering = ("id",)



from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    PrincipalProfile,
    TeacherProfile,
    StudentProfile,
)


@admin.register(PrincipalProfile)
class PrincipalProfileAdmin(ModelAdmin):

    list_display = (
        "id",
        "phone_number",
        "admin_level",
        "office_room",
        "designation",
        "user_id",
    )

    search_fields = (
        "user__username",       # ← fixed: double-underscore FK lookup
        "phone_number",
        "designation",
    )

    ordering = ("id",)

    # Unfold extras
    list_fullwidth = True
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(TeacherProfile)
class TeacherProfileAdmin(ModelAdmin):

    list_display = (
        "id",
        "phone_number",
        "experience",
        "qualification",
        "joining_date",
        "user_id",
    )

    search_fields = (
        "user__username",       # ← fixed: double-underscore FK lookup
        "qualification",
    )

    list_filter = (
        "qualification",
        "joining_date",
    )

    ordering = ("id",)

    readonly_fields = ("joining_date",)  # ← set on creation, not editable
    date_hierarchy = "joining_date"      # ← drill-down by join date

    # Unfold extras
    list_fullwidth = True
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(StudentProfile)
class StudentProfileAdmin(ModelAdmin):

    list_display = (
        "id",
        "roll_number",
        "admission_number",
        "address",
        "user_id",
        "academic_class_id",
    )

    search_fields = (
        "user__username",           # ← added: search by username
        "roll_number",              # ← added: useful for student lookup
        "admission_number",         # ← added: most common student identifier
    )

    list_filter = (
        "academic_class",
    )

    ordering = ("id",)

    # Unfold extras
    list_fullwidth = True
    compressed_fields = True
    warn_unsaved_form = True