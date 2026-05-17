from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Attendance
from .serializers import AttendanceSerializer
from profiles.models import StudentProfile
from drf_spectacular.utils import extend_schema
from accounts.models import User
from django.db import models

from .models import Attendance

class MarkAttendanceView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
    responses={201: "Created Successfully"}
)
    def post(self, request):

        if request.user.role != "teacher":
            return Response({"error": "Only teachers allowed"}, status=403)

        serializer = AttendanceSerializer(
            data=request.data,
            context={'request': request}
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=400)
    
    
    
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from attendance.models import Attendance


# class AttendanceSummaryView(APIView):

#     permission_classes = [IsAuthenticated]

#     @extend_schema(
#     responses={200: list}
# )
#     def get(self, request):

#         if request.user.role != "teacher":
#             return Response(
#                 {"error": "Only teachers allowed"},
#                 status=403
#             )

#         date = request.query_params.get('date')

#         attendance = Attendance.objects.filter(
#             marked_by=request.user,
#             date=date
#         )

#         present_count = attendance.filter(status='P').count()
#         absent_count = attendance.filter(status='A').count()

#         return Response({
#             "date": date,
#             "present": present_count,
#             "absent": absent_count,
            
#         })
        


class AttendanceSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role != "teacher":
            return Response({"error": "Only teachers allowed"}, status=403)

        date = request.query_params.get('date')

        attendance = Attendance.objects.filter(
            marked_by=request.user,
            date=date
        ).select_related("student__user")

        present_count = attendance.filter(status='P').count()
        absent_count = attendance.filter(status='A').count()

        records = [
            {
                "student_id": a.student.id,
                "student_name": a.student.user.username,
                "status": a.status
            }
            for a in attendance
        ]

        return Response({
            "date": date,
            "present": present_count,
            "absent": absent_count,
            "teacher": request.user.username,
            "records": records
        })


# attendance/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from django.db import models

from .models import Attendance
from profiles.models import StudentProfile


class MyAttendanceView(APIView):
    """
    View for students to see their own attendance records.
    Shows which days they were present, absent, or late.
    """
    
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: {
            "type": "object",
            "properties": {
                "student_id": {"type": "integer"},
                "student_name": {"type": "string"},
                "total_present": {"type": "integer"},
                "total_absent": {"type": "integer"},
                "total_late": {"type": "integer"},
                "attendance_percentage": {"type": "number"},
                "attendance_records": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "date": {"type": "string", "format": "date"},
                            "status": {"type": "string"},
                            "status_display": {"type": "string"},
                            "marked_by": {"type": "string"}
                        }
                    }
                }
            }
        }}
    )
    def get(self, request):
        # Check if the user is a student
        if request.user.role != "student":
            return Response(
                {"error": "Only students can view their own attendance"},
                status=403
            )
        
        # Get the student profile for this user
        try:
            student = StudentProfile.objects.get(user=request.user)
        except StudentProfile.DoesNotExist:
            return Response(
                {"error": "Student profile not found"},
                status=404
            )
        
        # Get all attendance records for this student, ordered by date (newest first)
        attendance_records = Attendance.objects.filter(
            student=student
        ).select_related('marked_by').order_by('-date')
        
        # Calculate statistics
        total_present = attendance_records.filter(status='P').count()
        total_absent = attendance_records.filter(status='A').count()
        total_late = attendance_records.filter(status='L').count()
        total_records = attendance_records.count()
        
        # Calculate attendance percentage (considering present and late as present? Adjust as needed)
        # Option 1: Only count 'P' as present
        attendance_percentage = 0
        if total_records > 0:
            attendance_percentage = (total_present / total_records) * 100
        
        # Option 2: Count both 'P' and 'L' as present (uncomment if preferred)
        # total_present_or_late = total_present + total_late
        # if total_records > 0:
        #     attendance_percentage = (total_present_or_late / total_records) * 100
        
        # Format attendance records
        records = []
        for record in attendance_records:
            status_display = {
                'P': 'Present',
                'A': 'Absent',
                'L': 'Late'
            }.get(record.status, 'Unknown')
            
            records.append({
                'date': record.date,
                'status': record.status,
                'status_display': status_display,
                'marked_by': record.marked_by.username if record.marked_by else 'Unknown',
                'marked_at': record.created_at if hasattr(record, 'created_at') else None
            })
        
        return Response({
            'student_id': student.id,
            'student_name': student.user.get_full_name() or student.user.username,
            'total_present': total_present,
            'total_absent': total_absent,
            'total_late': total_late,
            'total_records': total_records,
            'attendance_percentage': round(attendance_percentage, 2),
            'attendance_records': records
        })

class StudentAttendanceReportView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
    responses={200: list}
)
    def get(self, request, student_id):

        if request.user.role != "teacher":
            return Response(
                {"error": "Only teachers allowed"},
                status=403
            )

        try:
            student = StudentProfile.objects.get(id=student_id)
        except StudentProfile.DoesNotExist:
            return Response(
                {"error": "Student not found"},
                status=404
            )

        attendance = Attendance.objects.filter(student=student)

        total_present = attendance.filter(status='P').count()
        total_absent = attendance.filter(status='A').count()

        total = total_present + total_absent

        percentage = 0

        if total > 0:
            percentage = (total_present / total) * 100

        return Response({
            "student": student.user.username,
            "present": total_present,
            "absent": total_absent,
            "attendance_percentage": round(percentage, 2)
        })