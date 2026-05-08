
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
        
        
    def create(self, validate_data):
        user = User.objects.create_user(
            username = validate_data['username'],
            email = validate_data['email'],
            password=validate_data['password'],
            role = validate_data['role']
        )
        
        if user.role == 'PRINCIPAL':
            PrincipalProfile.objects.create(user=True)
            
        elif user.role == 'TEACHER':
            TeacherProfile.objects.create(user=True)
        
        elif user.role == 'STUDENT':
            StudentProfile.objects.create(user=True)
            
            
        return user