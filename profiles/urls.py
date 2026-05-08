



from django.urls import path
from .views import PrincipalProfileView, TeacherListCreateView, TeacherDetailView, StudentListCreateView

urlpatterns = [
     path('principal/profile/', PrincipalProfileView.as_view(), name='principal-profile'),
     path('teachers/', TeacherListCreateView.as_view(), name='teacher-list-create'),
     path('teachers/<int:pk>/', TeacherDetailView.as_view(), name='teacher-detail'),
     path('students/', StudentListCreateView.as_view(), name='student-list-create')
]
