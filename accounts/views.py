from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer
from .models import User
from rest_framework.permissions import AllowAny
from profiles.models import PrincipalProfile
from drf_spectacular.utils import extend_schema
# Create your views here.

# View = handles request

# class PrincipalRegisterView(APIView):
#     permission_classes = [AllowAny]
    
#     def post(self, request):
#         data = request.data.copy()
        
#         data['role'] = User.PRINCIPAL
        
        
#         serializer = RegisterSerializer(data=data)
        
#         if serializer.is_valid():
#             serializer.save()
            
            
#             return Response(
                
#                 {
#                     "message": "Principal registered successfully"
#                 },
#                 status=status.HTTP_201_CREATED
#             )
            
            
#         return Response(serializer.errors, status=400)
    
    
    
class PrincipalRegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer, responses={201: None})  # 👈 add this
    def post(self, request):

        # 🚨 Block second principal
        if User.objects.filter(role=User.PRINCIPAL).exists():
            return Response(
                {"error": "Principal already exists"},
                status=400
            )

        # create principal directly
        user = User.objects.create_user(
            username=request.data['username'],
            email=request.data['email'],
            password=request.data['password'],
            role=User.PRINCIPAL
        )

        # create profile
        PrincipalProfile.objects.create(user=user)

        return Response(
            {"message": "Principal created successfully"},
            status=201
        )
        


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterSerializer
from .models import User
from .permissions import IsPrincipal


class UserCreateView(APIView):
    permission_classes = [IsAuthenticated , IsPrincipal]
    
    @extend_schema(request=RegisterSerializer, responses={201: None})  # 👈 add this
    def post(self , request):
        
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
            
        return Response(serializer.errors, status=400)