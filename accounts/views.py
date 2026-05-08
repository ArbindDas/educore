from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import User
from rest_framework.permissions import AllowAny
# Create your views here.

# View = handles request
class PrincipalRegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        data = request.data.copy()
        
        data['role'] = User.PRINCIPAL
        
        
        serializer = RegisterSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
            
            
            return Response(
                
                {
                    "message": "Principal registered successfully"
                },
                status=status.HTTP_201_CREATED
            )
            
            
        return Response(serializer.errors, status=400)
    
    
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer
from .models import User
from .permissions import IsPrincipal

class UserCreateView(APIView):
    permission_classes = [IsAuthenticated , IsPrincipal]
    
    def post(self , request):
        
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors, status=400)