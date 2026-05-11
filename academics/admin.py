from django.contrib import admin

# Register your models here.



from .models import (
    AcademicClass,
    TeacherClassAssignment
)

@admin.register(AcademicClass)
class AcademicClassAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "name",
        "section"
    )
    
    
    search_fields = (
        "name",
        "section"
    )
    
   
    ordering = ("id",)
    
    
@admin.register(TeacherClassAssignment)
class TeacherClassAssignmentAdmin(admin.ModelAdmin):
    
    list_display =(
        "id",
        "subject",
        "academic_class_id",
        "teacher_id",
    )
    
    

    
    search_fields = (
        "teacher_username",
        "subject"
    )
    
    list_filter = (
        "academic_class_id",
        "subject"
    )
    
    
    ordering = ("id",)