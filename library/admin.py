# from django.contrib import admin

# # Register your models here.
# from .models import (
#     Book,
#     BookIssue
# )

# @admin.register(Book)
# class BookAdmin(admin.ModelAdmin):
   
#     list_display = (
#         "id",
#         "title",
#         "author",
#         "isbn",
#         "total_copies",
#         "available_copies",
#         "created_at",
#     )
    
#     search_fields = (
#         "title",
#         "author",
#         "isbn",
#     )
    
#     list_filter = (
#         "author",
#     )
    
#     ordering = ("title",)
    
    
    
# @admin.register(BookIssue)
# class BookIssueAdmin(admin.ModelAdmin):

#     list_display = (
#         "id",
#         "student",
#         "book",
#         "issued_by",
#         "issue_date",
#         "return_date",
#         "is_returned",
#     )

#     search_fields = (
#         "student__user__username",
#         "student__admission_number",
#         "book__title",
#         "book__isbn",
#         "issued_by__username",
#     )

#     list_filter = (
#         "is_returned",
#         "issue_date",
#         "book",
#     )

#     ordering = ("-issue_date",)
     
     
     
    


from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import (
    Book,
    BookIssue,
)


@admin.register(Book)
class BookAdmin(ModelAdmin):

    list_display = (
        "id",
        "title",
        "author",
        "isbn",
        "total_copies",
        "available_copies",
        "created_at",
    )

    search_fields = (
        "title",
        "author",
        "isbn",
    )

    list_filter = (
        "author",
    )

    ordering = ("title",)

    readonly_fields = ("created_at",)   # ← created_at should not be editable

    # Unfold extras
    list_fullwidth = True
    compressed_fields = True
    warn_unsaved_form = True


@admin.register(BookIssue)
class BookIssueAdmin(ModelAdmin):

    list_display = (
        "id",
        "student",
        "book",
        "issued_by",
        "issue_date",
        "return_date",
        "is_returned",
    )

    search_fields = (
        "student__user__username",
        "student__admission_number",
        "book__title",
        "book__isbn",
        "issued_by__username",
    )

    list_filter = (
        "is_returned",
        "issue_date",
        "book",
    )

    ordering = ("-issue_date",)

    readonly_fields = ("issue_date",)   # ← issue date is set on creation, not editable
    date_hierarchy = "issue_date"       # ← drill-down by year → month → day

    # Unfold extras
    list_fullwidth = True
    compressed_fields = True
    warn_unsaved_form = True