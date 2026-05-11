from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
class AcademicClass(models.Model):
    name = models.CharField(max_length=50)
    section = models.CharField(max_length=10)


class TeacherClassAssignment(models.Model):
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE
    )

    subject = models.CharField(max_length=100)
    
    def clean(self):
        if self.teacher.role != 'teacher':
            raise ValidationError (
                "Selected user is not a teacher"
            )
            
            
    def __str__(self):
        return f"{self.teacher.username} - {self.subject}"