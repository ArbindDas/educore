from django.contrib import admin

# Register your models here.



from .models import (
    PrincipalProfile,
    TeacherProfile,
    StudentProfile
)


@admin.register(PrincipalProfile)
class PrincipalProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "phone_number",
        "admin_level",
        "office_room",
        "designation",
        "user_id"
    )
    
    search_fields = (
        "user_username",
        "phone_number",
        "designation"
    )
    
    ordering = ("id",)
    

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "phone_number",
        "experience",
        "qualification",
        "joining_date",
        "user_id"
    )
    
    
    search_fields = (
        "user_username",
        "qualification",
    )
    
    list_filter = (
        "qualification",
        "joining_date",
    )
    
    ordering = ("id",)
    

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    
    list_display = (
        "id",
        "roll_number",
        "admission_number",
        "address",
        "user_id",
        "academic_class_id"
    )
    
    list_filter = (
        "academic_class",
    )

    ordering = ("id",)