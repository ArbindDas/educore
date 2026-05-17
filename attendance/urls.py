"""
URL configuration for educore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from . import views
urlpatterns = [
    
   path('attendance/mark/', views.MarkAttendanceView.as_view(), name='attandance-mark'),
   path(
    'attendance/summary/',
    views.AttendanceSummaryView.as_view(), name='attendance-summary'),
   
   
   path(
    'attendance/student/<int:student_id>/',
    views.StudentAttendanceReportView.as_view(),name='student-attendance-report'),
   
    path('attendance/my-attendance/', views.MyAttendanceView.as_view(), name='my-attendance'),  # Add this line
    
]