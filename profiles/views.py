from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profiles.models import PrincipalProfile, TeacherProfile, StudentProfile
from .serializers import PrincipalProfileSerializer
from .serializers import TeacherCreateSerializer, TeacherUpdateSerializer, StudentCreateSerializer, StudentUpdateSerializer
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
    
    # Get list all student OR single student
    def get(self , request):
        permission_classes = [IsAuthenticated]
        if request.user.role !='principal':
            return Response(
                {"error": "Not allowed"},
                status=403
            )
        
        student = StudentProfile.objects.all()
        data = []
        
        for s in student:
            data.append({
                'id':s.id,
                'class_name':s.class_name,
                'section': s.section,
                'roll_number': s.roll_number,
                'admission_number': s.admission_number,
                'address':s.address
            })
            
            
        return Response(data)
    
    
    
class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    #Get single student
    
    def get(self , request, pk):
        if request.user.role!= 'principal':
            return Response(
                {"error": "Not allowed"},
                status=403
            )
        try:
            student = StudentProfile.objects.get(id=pk)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student not found"}, status=404)
        
        return Response({
            'id':student.id,
            'class_name':student.class_name,
            'section': student.section,
            'roll_number': student.roll_number,
            'admission_number': student.admission_number,
            'address': student.address
        })
        
    def patch(self , request, pk):
        if request.user.role != 'principal':
            return Response(
                {"error": "Not allowed"},
                status=403
            )
    
        student = StudentProfile.objects.get(pk=pk)
        
        serailizer = StudentUpdateSerializer(
            student,
            data = request.data,
            partial=True
        )
        
        if serailizer.is_valid():
            serailizer.save()
            return Response({
                "message": "Student updated successfully",
                "data": serailizer.data
            })
            
        return Response(serailizer.errors, status=400)
    
    
    def delete(self , request, pk):
        if request.user.role != 'principal':
            return Response({"error": "Not allowed"}, status=403)
        
        try:
            student = StudentProfile.objects.get(id=pk)
        except StudentProfile.DoesNotExist:
            return Response({
                "error":"Student not found", 
            }, status=404)
            
        student.user.delete() # delete the linked user
        student.delete() # delete the student profile
        
        return Response({"message": "Student deleted"})
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
        
        if request.user.role != 'principal':
            return Response(
            {"error": "Not allowed"},
            status=403
        )

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
    
    
    # DELETE teacher
    def delete(self, request, pk):
        
        
        if request.user.role != 'principal':
            return Response(
            {"error": "Not allowed"},
            status=403
        )
            
        try:
            teacher = TeacherProfile.objects.get(id=pk)
        except TeacherProfile.DoesNotExist:
            return Response(
            {"error": "Teacher not found"},
            status=404
        )

        teacher.user.delete()   # deletes linked User
        teacher.delete()        # deletes TeacherProfile

        return Response({"message": "Teacher deleted"})
    
    

    
    