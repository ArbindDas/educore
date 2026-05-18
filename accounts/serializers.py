
from rest_framework import serializers
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from profiles.models import PrincipalProfile , TeacherProfile, StudentProfile



user = get_user_model()

# Serializer = creates object
# 👉 .save() = triggers create() internally

class RegisterSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(
        write_only = True,
        validators = [validate_password]
    )
    
    class Meta:
        model = user
        fields = ['username', 'email', 'password', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
        
    def create(self, validated_data):

        role = validated_data.get('role')

    # 🚨 Block principal creation from register API
        if role == User.PRINCIPAL:
            raise serializers.ValidationError("You cannot create principal via this API")

        user = User.objects.create_user(
        username=validated_data['username'],
        email=validated_data['email'],
        password=validated_data['password'],
        role=role
    )   

        # if user.role == User.TEACHER:
        #     TeacherProfile.objects.create(user=user)
        if user.role == 'TEACHER':
            TeacherProfile.objects.create(user=True)
        
        elif user.role == 'STUDENT':
            StudentProfile.objects.create(user=True)
            
        
    
        return user
        
  