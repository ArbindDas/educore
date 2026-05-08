
from rest_framework import serializers
from profiles.models import PrincipalProfile
from profiles.models import TeacherProfile
from accounts.models import User
from rest_framework import serializers
from accounts.models import User
from profiles.models import TeacherProfile

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
    
    
    
class TeacherUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = TeacherProfile
        fields = [
            'phone_number',
            'experience',
            'qualification',
            'subject'
        ]