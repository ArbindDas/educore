# from django.contrib import admin

# # Register your models here.


# from .models import Attendance
# @admin.register(Attendance)
# class AttendanceAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "date",
#         "created_at",
#         "academic_class",
#         "marked_by",
#         "student",
#     )

#     search_fields = (
#         "id",
#         "student__id",
#         "student__user__username",
#         "student__admission_number",
#         "academic_class__name",
#         "marked_by__username",
#     )

#     list_filter = (
#         "status",
#         "academic_class",
#         "date",
#     )

#     ordering = ("-date",)

#     readonly_fields = ("created_at",)




from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):

    list_display = (
        "id",
        "date",
        "created_at",
        "academic_class",
        "marked_by",
        "student",
        "status",          # ← added so status is visible in the list
    )

    search_fields = (
        "id",
        "student__id",
        "student__user__username",
        "student__admission_number",
        "academic_class__name",
        "marked_by__username",
    )

    list_filter = (
        "status",
        "academic_class",
        "date",
    )

    ordering = ("-date",)

    readonly_fields = ("created_at",)

    # Unfold extras
    list_fullwidth = True
    compressed_fields = True
    warn_unsaved_form = True
    date_hierarchy = "date"    # ← adds a clickable date drill-down bar at the top