
from rest_framework import serializers
from profiles.models import PrincipalProfile
from profiles.models import TeacherProfile
from accounts.models import User
from rest_framework import serializers
from accounts.models import User
from profiles.models import TeacherProfile, StudentProfile
from academics.models import AcademicClass


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
    
    

# class StudentCreateSerializer(serializers.ModelSerializer):
#     user_id = serializers.IntegerField()

#     class Meta:
#         model = StudentProfile
#         fields = [
#             'user_id',
#             'class_name',
#             'section',
#             'roll_number',
#             'admission_number',
#             'address'
#         ]

#     def create(self, validated_data):
#         user_id = validated_data.pop('user_id')

#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("User does not exist")

#         if user.role.lower() != "student":
#             raise serializers.ValidationError("User is not a student")

#         if hasattr(user, "student_profile"):
#             raise serializers.ValidationError("Student profile already exists")

#         student = StudentProfile.objects.create(
#             user=user,
#             **validated_data
#         )

#         return student
    
    
class StudentCreateSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()
    academic_class_id = serializers.IntegerField()

    class Meta:
        model = StudentProfile
        fields = [
            'user_id',
            'academic_class_id',
            'roll_number',
            'admission_number',
            'address'
        ]

    def create(self, validated_data):
        user_id = validated_data.pop('user_id')
        class_id = validated_data.pop('academic_class_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise serializers.ValidationError("User does not exist")

        if user.role.lower() != "student":
            raise serializers.ValidationError("User is not a student")

        if hasattr(user, "student_profile"):
            raise serializers.ValidationError("Student profile already exists")

        academic_class = AcademicClass.objects.get(id=class_id)

        student = StudentProfile.objects.create(
            user=user,
            academic_class=academic_class,
            **validated_data
        )

        return student
    
# class StudentProfileSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(source='user.username')
#     email = serializers.EmailField(source='user.email')

#     class Meta:
#         model = StudentProfile

#         fields = [
#             'username',
#             'email',
#             'class_name',
#             'section',
#             'roll_number',
#             'admission_number',
#             'address'
#         ]

class StudentProfileSerializer(serializers.ModelSerializer):

    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')

    academic_class = serializers.CharField(source='academic_class.name')
    section = serializers.CharField(source='academic_class.section')

    class Meta:
        model = StudentProfile

        fields = [
            'username',
            'email',
            'academic_class',
            'section',
            'roll_number',
            'admission_number',
            'address'
        ]

class TeacherProfileSerializer(serializers.ModelSerializer):
    
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    
    class Meta:
        model = TeacherProfile
        
        fields = [
            'username',
            'email',
            'phone_number',
            'experience',
            'qualification',
            
        ]
    
class TeacherUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherProfile
        fields = [
            'phone_number',
            'experience',
            'qualification',
            
        ]
        
        
        
class StudentUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProfile
        fields = [
            'roll_number',
            'admission_number',
            'address'
        ]
        
        
        
        
        
# class StudentUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model= StudentProfile
#         fields = [
#             'class_name',
#             'section',
#             'roll_number',
#             'admission_number',
#             'address'
#         ]   





from rest_framework import serializers
from academics.models import TeacherClassAssignment, AcademicClass
from accounts.models import User
class TeacherClassAssignmentSerializer(serializers.ModelSerializer):
    teacher_id = serializers.IntegerField()
    academic_class_id = serializers.IntegerField()

    class Meta:
        model = TeacherClassAssignment
        fields = [
            'teacher_id',
            'academic_class_id',
            'subject'
        ]

    def create(self, validated_data):
        teacher_id = validated_data.pop('teacher_id')
        class_id = validated_data.pop('academic_class_id')

        try:
            teacher = User.objects.get(id=teacher_id, role="teacher")
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid teacher")

        academic_class = AcademicClass.objects.get(id=class_id)

        return TeacherClassAssignment.objects.create(
            teacher=teacher,
            academic_class=academic_class,
            **validated_data
        )