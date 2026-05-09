



from django.urls import path
from .views import PrincipalProfileView, TeacherListCreateView, TeacherDetailView, StudentListCreateView , StudentDetailView,MyStudentProfileView , MyTeacherProfileView, AssignTeacherToClassView ,TeacherStudentsView

urlpatterns = [
     path('principal/profile/', PrincipalProfileView.as_view(), name='principal-profile'),
     path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
     path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
     path('students/', StudentListCreateView.as_view(), name='student-list-create'),
     path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
     path('student/me/', MyStudentProfileView.as_view(), name='my-student-profile'),
     path('teacher/me/', MyTeacherProfileView.as_view(), name='my-teacher-profile'),
     path(
        'teacher-assign/',
        AssignTeacherToClassView.as_view(),
        name='teacher-assign'
    ),
     
    path('teacher/students/', TeacherStudentsView.as_view(), name='teacher-student-view')
]


#http://127.0.0.1:8000/api/docs/ 