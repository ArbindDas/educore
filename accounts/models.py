from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    
    PRINCIPAL = 'principal'
    TEACHER = 'teacher'
    STUDENT =  'student'
    LIBRARIAN = 'librarian'
    
    
    ROLE_CHOICES = [
        (PRINCIPAL,'principal' ),
        (TEACHER,'teacher' ),
        (STUDENT, 'student'),
        (LIBRARIAN, 'librarian')
        
    ]
    
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    
    
    
    def __str__(self):
        return f'{self.username} - {self.role}'
