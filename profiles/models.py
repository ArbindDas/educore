from django.db import models
from accounts.models import User
from academics.models import AcademicClass
from django.conf import settings
class PrincipalProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='principal_profile'
        )
    phone_number = models.CharField(max_length=20)
    admin_level = models.CharField(max_length=50)
    office_room = models.CharField(max_length=10)
    designation = models.CharField(max_length=50)

    
    
    def __str__(self):
        return f'{self.user.username}'
    



# class TeacherProfile(models.Model):

#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name='teacher_profile'
#     )

#     phone_number = models.CharField(max_length=20)
#     experience = models.CharField(max_length=50)
#     qualification = models.CharField(max_length=100)

#     joining_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username

class TeacherProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile'
    )

    phone_number = models.CharField(max_length=20)
    experience = models.CharField(max_length=50)
    qualification = models.CharField(max_length=100)

    joining_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    def delete(self, *args, **kwargs):
        user = self.user
        super().delete(*args, **kwargs)
        user.delete()


class StudentProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    academic_class = models.ForeignKey(
        AcademicClass,
        on_delete=models.CASCADE
    )

    roll_number = models.PositiveIntegerField()

    admission_number = models.CharField(
        max_length=30,
        unique=True
    )

    address = models.TextField()

    def __str__(self):
        return self.user.username
    
    
    
    
    
    

# class TeacherProfile(models.Model):

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='teacher_profile'
#     )

#     phone_number = models.CharField(max_length=20)
#     experience = models.CharField(max_length=50)
#     qualification = models.CharField(max_length=100)
#     subject = models.CharField(max_length=50)

#     joining_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.user.username


# class StudentProfile(models.Model):

#     user = models.OneToOneField(
#         User,
#         on_delete=models.CASCADE,
#         related_name='student_profile'
#     )

#     class_name = models.CharField(max_length=50)
#     section = models.CharField(max_length=10)

#     roll_number = models.PositiveIntegerField()

#     admission_number = models.CharField(
#         max_length=30,
#         unique=True
#     )

#     address = models.TextField()

#     def __str__(self):
#         return self.user.username

