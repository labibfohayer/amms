from rest_framework import views, generics, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import StudentAttendance, TeacherAttendance, HostelNightAttendance
from .serializers import (
    StudentAttendanceSerializer, TeacherAttendanceSerializer,
    HostelNightAttendanceSerializer, BulkAttendanceSerializer
)
from apps.students.models import Student
from apps.academic.models import ClassRoom
from apps.teachers.models import Teacher
from apps.notifications.whatsapp import send_absent_notification

class IsPrincipalOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['principal', 'vice_principal', 'managing_director', 'teacher']

class IsPrincipal(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['principal', 'vice_principal', 'managing_director']

class StudentAttendanceBulkView(views.APIView):
    permission_classes = [IsPrincipalOrTeacher]
    
    def post(self, request):
        serializer = BulkAttendanceSerializer(data=request.data)
        if serializer.is_valid():
            classroom = get_object_or_404(ClassRoom, pk=serializer.validated_data['classroom_id'])
            date = serializer.validated_data['date']
            
            for item in serializer.validated_data['attendances']:
                student = get_object_or_404(Student, pk=item['student_id'])
                StudentAttendance.objects.update_or_create(
                    student=student, date=date, classroom=classroom,
                    defaults={'status': item['status'], 'taken_by': request.user}
                )
                if item['status'] == 'absent':
                    send_absent_notification(student, str(date))
            return Response({'status': 'Attendance saved'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentAttendanceListView(generics.ListAPIView):
    serializer_class = StudentAttendanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        qs = StudentAttendance.objects.all()
        date = self.request.query_params.get('date')
        classroom_id = self.request.query_params.get('classroom_id')
        student_id = self.request.query_params.get('student_id')
        
        if date:
            qs = qs.filter(date=date)
        if classroom_id:
            qs = qs.filter(classroom_id=classroom_id)
        if student_id:
            qs = qs.filter(student_id=student_id)
            
        if self.request.user.role == 'student':
            qs = qs.filter(student__user=self.request.user)
        elif self.request.user.role == 'guardian':
            qs = qs.filter(student__guardian_phone=self.request.user.phone)
            
        return qs

class StudentAttendanceMonthlyView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, student_id, month, year):
        qs = StudentAttendance.objects.filter(student_id=student_id, date__month=month, date__year=year)
        if request.user.role == 'student':
            student = get_object_or_404(Student, pk=student_id)
            if student.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
        elif request.user.role == 'guardian':
            student = get_object_or_404(Student, pk=student_id)
            if student.guardian_phone != request.user.phone:
                return Response(status=status.HTTP_403_FORBIDDEN)
        
        data = {
            'total': qs.count(),
            'present': qs.filter(status='present').count(),
            'absent': qs.filter(status='absent').count(),
            'late': qs.filter(status='late').count(),
            'leave': qs.filter(status='leave').count(),
        }
        return Response(data)

class TeacherAttendanceBulkView(views.APIView):
    permission_classes = [IsPrincipal]
    
    def post(self, request):
        date = request.data.get('date')
        attendances = request.data.get('attendances', [])
        for item in attendances:
            teacher = get_object_or_404(Teacher, pk=item['teacher_id'])
            TeacherAttendance.objects.update_or_create(
                teacher=teacher, date=date,
                defaults={'status': item['status']}
            )
        return Response({'status': 'Teacher attendance saved'})

class HostelAttendanceView(generics.ListCreateAPIView):
    serializer_class = HostelNightAttendanceSerializer
    queryset = HostelNightAttendance.objects.all()
    permission_classes = [IsPrincipalOrTeacher]

class AttendanceReportView(views.APIView):
    permission_classes = [IsPrincipalOrTeacher]
    def get(self, request):
        # placeholder report
        return Response({'status': 'Report data goes here'})
