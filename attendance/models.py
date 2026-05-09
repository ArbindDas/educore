from django.db import models
from profiles.models import StudentProfile
from academics.models import AcademicClass
from accounts.models import User


class Attendance(models.Model):

    STATUS_CHOICES = [
        ('P', 'Present'),
        ('A', 'Absent'),
    ]

    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    academic_class = models.ForeignKey(AcademicClass, on_delete=models.CASCADE)

    date = models.DateField()

    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    marked_by = models.ForeignKey(User, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'date')  # IMPORTANT

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {self.status}"