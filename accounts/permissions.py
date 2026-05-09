
# ✅ STEP 1: Create Permission (VERY IMPORTANT)


from rest_framework.permissions import BasePermission
from .models import User

class IsPrincipal(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated and
            request.user.role == 'principal'
        )
        



class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            (
                request.user.role == 'student' 
            )
        )
        

class IsTeacher(BasePermission):
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated and
            (
                request.user.role == 'teacher'
            )
        )
        
# class IsStudent(BasePermission):
#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated and
#             request.user.role in ['student', 'principal']
#         )