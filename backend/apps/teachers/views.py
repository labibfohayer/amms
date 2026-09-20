from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Teacher, SalaryPayment, LeaveApplication
from .serializers import (TeacherListSerializer, TeacherDetailSerializer, 
                          TeacherCreateSerializer, SalaryPaymentSerializer, 
                          LeaveApplicationSerializer)
from .utils import generate_id_card_pdf, generate_salary_slip_pdf

class IsPrincipal(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['principal', 'vice_principal', 'managing_director']

class TeacherListCreateView(generics.ListCreateAPIView):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TeacherCreateSerializer
        return TeacherListSerializer

    def get_queryset(self):
        return Teacher.objects.all()
        
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsPrincipal()]
        return [permissions.IsAuthenticated()]

class TeacherDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = TeacherDetailSerializer
    queryset = Teacher.objects.all()

    def get_queryset(self):
        if self.request.user.role in ['principal', 'vice_principal', 'managing_director']:
            return Teacher.objects.all()
        return Teacher.objects.filter(user=self.request.user)

class TeacherStatusUpdateView(views.APIView):
    permission_classes = [IsPrincipal]

    def post(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        teacher.is_active = not teacher.is_active
        teacher.save()
        return Response({'status': 'Teacher status updated', 'is_active': teacher.is_active})

class SalaryPaymentView(views.APIView):
    permission_classes = [IsPrincipal]
    
    def post(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        serializer = SalaryPaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(teacher=teacher, paid_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherSalaryStatusView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        if request.user.role not in ['principal', 'vice_principal', 'managing_director'] and request.user != teacher.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
            
        payments = SalaryPayment.objects.filter(teacher=teacher)
        serializer = SalaryPaymentSerializer(payments, many=True)
        return Response(serializer.data)

class TeacherIDCardView(views.APIView):
    def get(self, request, pk):
        teacher = get_object_or_404(Teacher, pk=pk)
        return generate_id_card_pdf(teacher)

class SalarySlipView(views.APIView):
    def get(self, request, pk, month, year):
        teacher = get_object_or_404(Teacher, pk=pk)
        payment = get_object_or_404(SalaryPayment, teacher=teacher, month=month, year=year)
        return generate_salary_slip_pdf(teacher, month, year, payment)

class LeaveApplicationView(generics.ListCreateAPIView):
    serializer_class = LeaveApplicationSerializer
    
    def get_queryset(self):
        if self.request.user.role in ['principal', 'vice_principal', 'managing_director']:
            return LeaveApplication.objects.all()
        # assume teacher profile exists
        return LeaveApplication.objects.filter(teacher__user=self.request.user)
        
    def perform_create(self, serializer):
        teacher = get_object_or_404(Teacher, user=self.request.user)
        serializer.save(teacher=teacher)

class LeaveReviewView(views.APIView):
    permission_classes = [IsPrincipal]
    
    def put(self, request, pk):
        leave = get_object_or_404(LeaveApplication, pk=pk)
        action = request.data.get('status')
        if action in ['approved', 'rejected']:
            leave.status = action
            leave.reviewed_by = request.user
            leave.save()
            return Response({'status': f'Leave {action}'})
        return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
