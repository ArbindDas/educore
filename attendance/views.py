from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Attendance
from .serializers import AttendanceSerializer
from profiles.models import StudentProfile
from drf_spectacular.utils import extend_schema


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


class AttendanceSummaryView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
    responses={200: list}
)
    def get(self, request):

        if request.user.role != "teacher":
            return Response(
                {"error": "Only teachers allowed"},
                status=403
            )

        date = request.query_params.get('date')

        attendance = Attendance.objects.filter(
            marked_by=request.user,
            date=date
        )

        present_count = attendance.filter(status='P').count()
        absent_count = attendance.filter(status='A').count()

        return Response({
            "date": date,
            "present": present_count,
            "absent": absent_count
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