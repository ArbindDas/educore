
from rest_framework import serializers
from profiles.models import PrincipalProfile
from profiles.models import TeacherProfile
from accounts.models import User
from rest_framework import serializers
from accounts.models import User
from profiles.models import TeacherProfile, StudentProfile


class PrincipalProfileSerializer (serializers.ModelSerializer):
    
    class Meta:
        model = PrincipalProfile
        fields = [
            'phone_number',
            'admin_level',
            'office_room',
            'designation'
        ]
        

class TeacherCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = TeacherProfile
        fields = [
            'user_id',
            'phone_number',
            'experience',
            'qualification',
            'subject'
        ]

    def create(self, validated_data):

        user_id = validated_data.pop('user_id')

        try:
            user = User.objects.get(id=user_id, role="TEACHER")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid teacher user")

        if hasattr(user, "teacher_profile"):
            raise serializers.ValidationError("Teacher profile already exists")

        teacher = TeacherProfile.objects.create(
            user=user,
            **validated_data
        )

        return teacher
    
    

class StudentCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = StudentProfile
        fields = [
            'user_id',
            'class_name',
            'section',
            'roll_number',
            'admission_number',
            'address'
        ]

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        if user.role.lower() != "student":
            raise serializers.ValidationError("User is not a student")

        if hasattr(user, "student_profile"):
            raise serializers.ValidationError("Student profile already exists")

        student = StudentProfile.objects.create(
            user=user,
            **validated_data
        )

        return student
class TeacherUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherProfile
        fields = [
            'phone_number',
            'experience',
            'qualification',
            'subject'
        ]
        
        
class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= StudentProfile
        fields = [
            'class_name',
            'section',
            'roll_number',
            'admission_number',
            'address'
        ]

