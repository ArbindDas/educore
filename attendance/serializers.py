from rest_framework import serializers
from .models import Attendance
from profiles.models import StudentProfile


class AttendanceSerializer(serializers.ModelSerializer):

    student_id = serializers.IntegerField()

    class Meta:
        model = Attendance
        fields = ['student_id', 'date', 'status']

    def create(self, validated_data):
        student_id = validated_data.pop('student_id')

        student = StudentProfile.objects.get(id=student_id)

        return Attendance.objects.create(
            student=student,
            academic_class=student.academic_class,
            marked_by=self.context['request'].user,
            **validated_data
        )