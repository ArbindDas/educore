from django.contrib import admin

# Register your models here.
from .models import (
    Book,
    BookIssue
)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
   
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
    
    
    
@admin.register(BookIssue)
class BookIssueAdmin(admin.ModelAdmin):

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
     
     
     
    
