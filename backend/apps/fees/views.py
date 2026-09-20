from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from .models import FeePayment, FeeReminder
from .serializers import FeePaymentSerializer, FeeCollectionSerializer, StudentFeeStatusSerializer, FeeReportSerializer
from .utils import generate_receipt_number, generate_receipt_pdf, BANGLA_MONTHS
from django.http import HttpResponse
from apps.notifications.whatsapp import send_fee_reminder
from apps.students.models import Student
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from datetime import date
from decimal import Decimal

class IsPrincipal(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'role', '') in ['principal', 'vice_principal', 'managing_director'])

class FeePaymentListView(generics.ListAPIView):
    serializer_class = FeePaymentSerializer
    queryset = FeePayment.objects.all()

class FeeCollectionView(generics.CreateAPIView):
    serializer_class = FeeCollectionSerializer
    def perform_create(self, serializer):
        serializer.save(
            receipt_number=generate_receipt_number(),
            collected_by=self.request.user
        )

class StudentFeeStatusView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, student_id):
        student = get_object_or_404(Student, student_id=student_id)
        
        # Access control
        if request.user.role not in ['principal', 'vice_principal', 'managing_director']:
            if request.user.role == 'student':
                if getattr(student, 'user', None) != request.user:
                    return Response(status=status.HTTP_403_FORBIDDEN)
            elif request.user.role == 'guardian':
                if getattr(student, 'guardian_phone', None) != getattr(request.user, 'phone', None):
                    return Response(status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(status=status.HTTP_403_FORBIDDEN)
        
        current_year = date.today().year
        current_month = date.today().month
        
        payments = FeePayment.objects.filter(student=student, payment_type='monthly', year=current_year)
        
        paid_months_data = []
        paid_month_numbers = set()
        total_paid_this_year = Decimal('0.00')
        
        for p in payments:
            if p.month:
                paid_month_numbers.add(p.month)
                paid_months_data.append({
                    "month": p.month,
                    "month_name": BANGLA_MONTHS.get(p.month, str(p.month)),
                    "amount_paid": p.amount_paid,
                    "payment_date": p.payment_date.strftime("%Y-%m-%d") if p.payment_date else None,
                    "receipt_number": p.receipt_number
                })
            total_paid_this_year += p.amount_paid
            
        due_months_data = []
        total_due_this_year = Decimal('0.00')
        
        for m in range(1, current_month + 1):
            if m not in paid_month_numbers:
                due_months_data.append({
                    "month": m,
                    "month_name": BANGLA_MONTHS.get(m, str(m)),
                    "amount_due": student.monthly_fee
                })
                total_due_this_year += student.monthly_fee
                
        # Handle hostel fee if applicable (Task didn't specify format for hostel dues in this view, so stick to monthly + returning hostel_fee as requested)
        return Response({
            "student_id": student.student_id,
            "name": student.name,
            "monthly_fee": student.monthly_fee,
            "hostel_fee": student.hostel_fee,
            "current_year": current_year,
            "paid_months": paid_months_data,
            "due_months": due_months_data,
            "total_paid_this_year": total_paid_this_year,
            "total_due_this_year": total_due_this_year
        })

class FeeReceiptPDFView(views.APIView):
    def get(self, request, pk):
        payment = generics.get_object_or_404(FeePayment, pk=pk)
        pdf = generate_receipt_pdf(payment)
        response = HttpResponse(pdf, content_type='application/pdf')
        return response

class DueFeeListView(views.APIView):
    permission_classes = [IsPrincipal]
    
    def get(self, request):
        current_year = date.today().year
        current_month = date.today().month
        
        students = Student.objects.filter(status='active').select_related('islamic_department', 'general_department')
        
        due_list = []
        for s in students:
            # Monthly fees
            expected_monthly = s.monthly_fee * current_month
            paid_monthly = FeePayment.objects.filter(student=s, payment_type='monthly', year=current_year).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
            monthly_due = expected_monthly - paid_monthly
            
            # Find exact due months for monthly fee
            paid_months = set(FeePayment.objects.filter(student=s, payment_type='monthly', year=current_year).values_list('month', flat=True))
            due_months = [BANGLA_MONTHS.get(m, str(m)) for m in range(1, current_month + 1) if m not in paid_months]
            
            # Hostel fees
            hostel_due = Decimal('0.00')
            if s.residential_status == 'residential':
                expected_hostel = s.hostel_fee * current_month
                paid_hostel = FeePayment.objects.filter(student=s, payment_type='hostel', year=current_year).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
                hostel_due = expected_hostel - paid_hostel
                
            total_due = monthly_due + hostel_due
            
            if total_due > 0:
                class_name = s.islamic_department.name if s.islamic_department else (s.general_department.name if s.general_department else '')
                due_list.append({
                    "student_id": s.student_id,
                    "name": s.name,
                    "name_bn": s.name_bn,
                    "class_name": class_name,
                    "guardian_phone": s.guardian_phone,
                    "total_due": total_due,
                    "due_months": due_months
                })
                
        # Sort descending by due amount
        due_list.sort(key=lambda x: x['total_due'], reverse=True)
        return Response(due_list)

class SendFeeReminderView(views.APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        student = get_object_or_404(Student, id=student_id)
        current_year = date.today().year
        current_month = date.today().month
        paid_months = set(FeePayment.objects.filter(student=student, payment_type='monthly', year=current_year).values_list('month', flat=True))
        due_months = [m for m in range(1, current_month + 1) if m not in paid_months]
        if due_months:
            first_due = due_months[0]
            month_name = BANGLA_MONTHS.get(first_due, str(first_due))
            send_fee_reminder(student, month_name, student.monthly_fee)
            return Response({'status': 'sent', 'month': month_name, 'amount': student.monthly_fee})
        return Response({'status': 'no dues'}, status=400)

class AllStudentsFeeReportView(views.APIView):
    def get(self, request):
        current_year = date.today().year
        current_month = date.today().month
        students = Student.objects.filter(status='active').select_related('islamic_department', 'general_department')
        report_data = []
        for s in students:
            expected_monthly = s.monthly_fee * current_month
            paid_monthly = FeePayment.objects.filter(student=s, payment_type='monthly', year=current_year).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
            monthly_due = expected_monthly - paid_monthly
            
            hostel_due = Decimal('0.00')
            paid_hostel = Decimal('0.00')
            if s.residential_status == 'residential':
                expected_hostel = s.hostel_fee * current_month
                paid_hostel = FeePayment.objects.filter(student=s, payment_type='hostel', year=current_year).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0.00')
                hostel_due = expected_hostel - paid_hostel
                
            report_data.append({
                "student_id": s.student_id,
                "name": s.name,
                "monthly_fee": s.monthly_fee,
                "total_paid_monthly": paid_monthly,
                "monthly_due": monthly_due,
                "hostel_fee": s.hostel_fee,
                "total_paid_hostel": paid_hostel,
                "hostel_due": hostel_due,
                "total_due": monthly_due + hostel_due
            })
        return Response(report_data)
