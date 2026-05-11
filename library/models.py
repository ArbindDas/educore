from django.db import models
from django.conf import settings
from profiles.models import StudentProfile


class Book(models.Model):

    title = models.CharField(max_length=200)

    author = models.CharField(max_length=100)

    isbn = models.CharField(
        max_length=20,
        unique=True
    )

    total_copies = models.PositiveIntegerField()

    available_copies = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BookIssue(models.Model):

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE
    )

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE
    )

    issued_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    issue_date = models.DateField(auto_now_add=True)

    return_date = models.DateField(
        null=True,
        blank=True
    )

    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.user.username} - {self.book.title}"