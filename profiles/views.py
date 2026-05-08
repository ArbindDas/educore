from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profiles.models import PrincipalProfile, TeacherProfile
from .serializers import PrincipalProfileSerializer
from .serializers import TeacherCreateSerializer, TeacherUpdateSerializer, StudentCreateSerializer
# Create your views here.


class PrincipalProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile, created = PrincipalProfile.objects.get_or_create(
            user=request.user
        )

        serializer = PrincipalProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        profile, created = PrincipalProfile.objects.get_or_create(
            user=request.user
        )

        serializer = PrincipalProfileSerializer(
            profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Profile updated successfully",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)
    
    
    
    
class StudentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        if request.user.role.lower() != 'principal':
            return Response(
                {"error": "Not allowed"},
                status=403
            )

        serializer = StudentCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {
                    "message": "Student profile created",
                    "data": serializer.data
                },
                status=201
            )

        print(serializer.errors)   # 👈 ADD THIS

        return Response(serializer.errors, status=400)
    
class TeacherListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    
    # Get list all teachers OR single teacher
    def get(self , request):
        if request.user.role != 'principal':
            return Response(
                {"error": "Not Allowed"},
                status=403
            )
        teachers = TeacherProfile.objects.all()
        data = []
        
        for t in teachers:
            data.append({
                'id': t.id,
                'phone_number': t.phone_number,
                'experience': t.experience,
                'qualification': t.qualification,
                'subject': t.subject
            })
            
        return Response(data)

    
    
    def post(self, request):
        
        # only principal allowed
        if request.user.role!='principal':
            return Response({"error": "Not Allowed"}, status=403)
        
        serializer = TeacherCreateSerializer(data=request.data)
        
        
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Teacher profile created",
                    "data": serializer.data
                    },
                
                )
        
        
        return Response(serializer.errors, status=400)
    
    
class TeacherDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    # ✔ GET single teacher
    def get(self, request, pk):

        if request.user.role != 'principal':
            return Response({"error": "Not Allowed"}, status=403)

        try:
            teacher = TeacherProfile.objects.get(id=pk)
        except TeacherProfile.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=404)

        return Response({
            "id": teacher.id,
            "phone_number": teacher.phone_number,
            "experience": teacher.experience,
            "qualification": teacher.qualification,
            "subject": teacher.subject
        })
    
    
    # PATCH update teacher
    def patch(self, request, pk):

        teacher = TeacherProfile.objects.get(id=pk)

        serializer = TeacherUpdateSerializer(
            teacher,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Teacher updated successfully",
                "data": serializer.data
            })

        return Response(serializer.errors, status=400)
    # 🔹 DELETE (remove teacher)
    
    # DELETE teacher
    def delete(self, request, pk):

        teacher = TeacherProfile.objects.get(id=pk)
        teacher.user.delete()
        teacher.delete()

        return Response({"message": "Teacher deleted"})
    
    

    
    