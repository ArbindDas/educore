from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from profiles.models import PrincipalProfile, TeacherProfile, StudentProfile
from .serializers import PrincipalProfileSerializer
from .serializers import (
    PrincipalProfileSerializer,
    TeacherCreateSerializer,
    TeacherUpdateSerializer,
    StudentCreateSerializer,
    StudentUpdateSerializer,
)
from drf_spectacular.utils import extend_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import StudentProfile
from .serializers import StudentProfileSerializer, TeacherProfileSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from academics.models import TeacherClassAssignment
from profiles.models import StudentProfile
from profiles.serializers import StudentProfileSerializer


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from academics.models import TeacherClassAssignment
from .serializers import TeacherClassAssignmentSerializer
class MyStudentProfileView(APIView):

    permission_classes = [IsAuthenticated]
    
    
    @extend_schema(
    responses={200: list}
)
    def get(self, request):
        
        
        if request.user.role != "student":
            return Response(
        {"error": "Only students can access this"},
        status=403
    )

        try:
            student_profile = StudentProfile.objects.get(
                user=request.user
            )

            serializer = StudentProfileSerializer(student_profile)

            return Response(serializer.data)

        except StudentProfile.DoesNotExist:
            return Response(
                {"error": "Student profile not found"},
                status=404
            )



class MyTeacherProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    @extend_schema(
    responses={200: list}
)
    def get(self, request):
        if request.user.role != 'teacher':
            return Response(
                {"error": "Not allowed"},
                status=403
            )
        try:
            teacher_profile = TeacherProfile.objects.get(
                user = request.user
            )
            
            serializer = TeacherProfileSerializer(teacher_profile)
             
            return Response(serializer.data)
        except TeacherProfile.DoesNotExist:
            return Response(
                {"error": "Teacher not Found"},
                status=404
            )

# ─────────────────────────────────────────────
# PRINCIPAL
# ─────

class PrincipalProfileView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=PrincipalProfileSerializer)  # GET
    def get(self, request):
        profile, created = PrincipalProfile.objects.get_or_create(
            user=request.user
        )

        serializer = PrincipalProfileSerializer(profile)
        return Response(serializer.data)

    @extend_schema(request=PrincipalProfileSerializer, responses=PrincipalProfileSerializer)  # ✅ fixed: was missing request=
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
    
    
# ─────────────────────────────────────────────
# STUDENT LIST + CREATE
# ─────────────────────────────────────────────
    
class StudentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    
    @extend_schema(request=StudentCreateSerializer, responses={201: None})
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
    @extend_schema(
    responses={200: list}
)
    # def get(self , request):
    #     permission_classes = [IsAuthenticated]
    #     if request.user.role !='principal':
    #         return Response(
    #             {"error": "Not allowed"},
    #             status=403
    #         )
        
    #     student = StudentProfile.objects.all()
    #     data = []
        
    #     for s in student:
    #         data.append({
    #             'id':s.id,
    #             'class_name':s.class_name,
    #             'section': s.section,
    #             'roll_number': s.roll_number,
    #             'admission_number': s.admission_number,
    #             'address':s.address
    #         })
            
            
    #     return Response(data)
    def get(self, request):

        if request.user.role != 'principal':
            return Response({"error": "Not allowed"}, status=403)

        students = StudentProfile.objects.select_related('academic_class').all()

        data = []

        for s in students:
            data.append({
                "id": s.id,
                "class_name": s.academic_class.name,  # ✅ correct
                "roll_number": s.roll_number,
                "admission_number": s.admission_number,
                "address": s.address
            })

        return Response(data)
    
    
# ─────────────────────────────────────────────
# STUDENT DETAIL (get, patch, delete)
# ─────────────────────────────────────────────
 
class StudentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    #Get single student
    @extend_schema(
    responses={200: list}
)
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
        
        # return Response({
        #     'id':student.id,
        #     'class_name':student.class_name,
        #     'section': student.section,
        #     'roll_number': student.roll_number,
        #     'admission_number': student.admission_number,
        #     'address': student.address
        # })
        
        return Response({
            'id': student.id,
            'class_name': student.academic_class.name,
            'roll_number': student.roll_number,
            'address': student.address
        })
        
    @extend_schema(request=StudentUpdateSerializer, responses=StudentUpdateSerializer)
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
    
    
    @extend_schema(responses={204: None})
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
    
# ─────────────────────────────────────────────
# TEACHER LIST + CREATE
# ─────────────────────────────────────────────
 
 
class TeacherListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    
    # Get list all teachers OR single teacher
    @extend_schema(
    responses={200: list}
)
    # def get(self , request):
    #     if request.user.role != 'principal':
    #         return Response(
    #             {"error": "Not Allowed"},
    #             status=403
    #         )
    #     teachers = TeacherProfile.objects.all()
    #     data = []
        
    #     for t in teachers:
    #         data.append({
    #             'id': t.id,
    #             'phone_number': t.phone_number,
    #             'experience': t.experience,
    #             'qualification': t.qualification,
    #             'subject': t.subject
    #         })
            
    #     return Response(data)
    def get(self, request):
        if request.user.role != 'principal':
            return Response({"error": "Not Allowed"}, status=403)

        teachers = TeacherProfile.objects.all()
        data = []

        for t in teachers:
            data.append({
            "id": t.id,
            "phone_number": t.phone_number,
            "experience": t.experience,
            "qualification": t.qualification,
            "username": t.user.username
        })

        return Response(data)

    
    
    @extend_schema(request=TeacherCreateSerializer, responses={201: None})
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
    
# ─────────────────────────────────────────────
# TEACHER DETAIL (get, patch, delete)
# ────────


class TeacherDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    
    # ✔ GET single teacher
    
    @extend_schema(
    responses={200: list}
)
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
            "username": teacher.user.username,
        })
    
    
    # PATCH update teacher
    @extend_schema(request=TeacherUpdateSerializer, responses=TeacherUpdateSerializer)
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
    @extend_schema(responses={204: None})
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
    
    

    
    



class AssignTeacherToClassView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(request=TeacherClassAssignmentSerializer, responses={201: None})
    def post(self, request):

        # (IMPORTANT) Only principal can assign
        if request.user.role != "principal":
            return Response(
                {"error": "Only principal can assign teachers"},
                status=403
            )

        serializer = TeacherClassAssignmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)

        return Response(serializer.errors, status=400)
    
    
    



class TeacherStudentsView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(
    responses={200: list}
)
    def get(self, request):

        if request.user.role != "teacher":
            return Response({"error": "Only teachers allowed"}, status=403)

        class_ids = TeacherClassAssignment.objects.filter(
            teacher=request.user
        ).values_list('academic_class_id', flat=True)

        students = StudentProfile.objects.filter(
            academic_class_id__in=class_ids
        )

        serializer = StudentProfileSerializer(students, many=True)

        return Response(serializer.data)