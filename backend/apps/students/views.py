from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.http import HttpResponse
from .models import Department, Student
from .serializers import (
    DepartmentSerializer, StudentListSerializer, StudentDetailSerializer,
    StudentAdmissionSerializer, StudentUpdateSerializer
)
from apps.accounts.permissions import IsPrincipal, IsPrincipalOrTeacher
from .utils import generate_id_card_pdf
from django.shortcuts import get_object_or_404

class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated]

class StudentListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StudentAdmissionSerializer
        return StudentListSerializer
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['principal', 'vice_principal', 'managing_director', 'teacher', 'staff']:
            return Student.objects.all()
        elif user.role == 'student':
            return Student.objects.filter(user=user)
        elif user.role == 'guardian':
            return Student.objects.filter(guardian_phone=user.phone)
        return Student.objects.none()
        
    def check_permissions(self, request):
        super().check_permissions(request)
        if request.method == 'POST':
            if request.user.role not in ['principal', 'vice_principal', 'managing_director', 'teacher']:
                self.permission_denied(request, message="Only principal or teacher can admit students.")

class StudentDetailView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['principal', 'vice_principal', 'managing_director', 'teacher', 'staff']:
            return Student.objects.all()
        elif user.role == 'student':
            return Student.objects.filter(user=user)
        elif user.role == 'guardian':
            return Student.objects.filter(guardian_phone=user.phone)
        return Student.objects.none()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return StudentUpdateSerializer
        return StudentDetailSerializer
        
    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)
        if request.method in ['PUT', 'PATCH'] and request.user.role not in ['principal', 'vice_principal', 'managing_director', 'teacher']:
            self.permission_denied(request, message="Only principal or teacher can edit.")



class StudentStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsPrincipal]
    
    def post(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        new_status = request.data.get('status')
        if new_status in dict(Student.STATUS_CHOICES):
            student.status = new_status
            if new_status == 'expelled':
                student.expulsion_reason = request.data.get('expulsion_reason', '')
            student.save()
            return Response({'detail': f'Status updated to {new_status}'})
        return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

class StudentIDCardView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, pk):
        student = get_object_or_404(Student, pk=pk)
        
        user = request.user
        if user.role not in ['principal', 'vice_principal', 'managing_director', 'teacher', 'staff']:
            if user.role == 'student' and student.user != user:
                return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
            if user.role == 'guardian' and student.guardian_phone != user.phone:
                return Response({'detail': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)
                
        pdf_bytes = generate_id_card_pdf(student)
        
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="student_id_{student.student_id}.pdf"'
        return response
