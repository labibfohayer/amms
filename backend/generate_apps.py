import os
from pathlib import Path

BASE_DIR = Path('C:/Users/assdi/.gemini/antigravity/scratch/amms/backend')

def create_file(path, content):
    p = BASE_DIR / path
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)

# 1. Notifications App
create_file('apps/notifications/__init__.py', '')
create_file('apps/notifications/apps.py', '''from django.apps import AppConfig

class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.notifications'
''')
create_file('apps/notifications/whatsapp.py', '''import requests
import os

WHATSAPP_SERVICE_URL = os.getenv('WHATSAPP_SERVICE_URL', 'http://localhost:3001')

def send_whatsapp_message(phone: str, message: str) -> bool:
    try:
        formatted = f"880{phone[1:]}" if phone.startswith('0') else phone
        response = requests.post(
            f"{WHATSAPP_SERVICE_URL}/send",
            json={"phone": formatted, "message": message},
            timeout=10
        )
        return response.status_code == 200
    except Exception as e:
        print(f"WhatsApp send failed: {e}")
        return False

def send_admission_notification(student, password: str):
    message = (
        f"আস-সালামু আলাইকুম!\\n\\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\\n"
        f"আপনার সন্তান *{student.name_bn or student.name}* এর ভর্তি সম্পন্ন হয়েছে।\\n\\n"
        f"*Student ID:* {student.student_id}\\n"
        f"*Password:* {password}\\n\\n"
        f"এই ID ও Password দিয়ে App-এ Login করুন।\\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(student.guardian_phone, message)

def send_absent_notification(student, date_str: str):
    message = (
        f"আস-সালামু আলাইকুম!\\n\\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\\n"
        f"আজ *{date_str}* তারিখে আপনার সন্তান\\n"
        f"*{student.name_bn or student.name}* মাদ্রাসায় অনুপস্থিত ছিলেন।\\n\\n"
        f"কোনো সমস্যা থাকলে মাদ্রাসায় যোগাযোগ করুন।\\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(student.guardian_phone, message)

def send_fee_reminder(student, month_name: str, amount: float):
    message = (
        f"আস-সালামু আলাইকুম!\\n\\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\\n"
        f"বিনীত স্মরণ করিয়ে দেওয়া যাচ্ছে যে,\\n"
        f"*{student.name_bn or student.name}* এর *{month_name}* মাসের\\n"
        f"বেতন *৳{amount}* এখনো পরিশোধিত হয়নি।\\n\\n"
        f"অনুগ্রহ করে দ্রুত পরিশোধ করুন।\\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(student.guardian_phone, message)

def send_result_notification(student, exam_name: str, gpa: float):
    message = (
        f"আস-সালামু আলাইকুম!\\n\\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\\n"
        f"*{student.name_bn or student.name}* এর\\n"
        f"*{exam_name}* এর ফলাফল প্রকাশিত হয়েছে।\\n\\n"
        f"*GPA:* {gpa}\\n\\n"
        f"App-এ Login করে বিস্তারিত দেখুন।\\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(student.guardian_phone, message)

def send_notice_broadcast(phones: list, title: str, body: str):
    message = (
        f"আস-সালামু আলাইকুম!\\n\\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\\n"
        f"*📢 নোটিশ: {title}*\\n\\n"
        f"{body}\\n\\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    success_count = 0
    for phone in phones:
        if send_whatsapp_message(phone, message):
            success_count += 1
    return success_count

def send_teacher_credentials(teacher, password: str):
    message = (
        f"আস-সালামু আলাইকুম!\\n\\n"
        f"*আল মদিনা মডেল মাদ্রাসা*\\n"
        f"আপনার অ্যাকাউন্ট তৈরি হয়েছে।\\n\\n"
        f"*Teacher ID:* {teacher.teacher_id}\\n"
        f"*Password:* {password}\\n\\n"
        f"এই ID ও Password দিয়ে App-এ Login করুন।\\n"
        f"জাযাকাল্লাহু খাইরান।"
    )
    return send_whatsapp_message(teacher.phone, message)
''')

# 2. Fees App
create_file('apps/fees/models.py', '''from django.db import models
from django.conf import settings

class FeePayment(models.Model):
    PAYMENT_STATUS = [
        ('paid', 'Paid - পরিশোধিত'),
        ('partial', 'Partial - আংশিক'),
    ]
    PAYMENT_TYPE = [
        ('monthly', 'Monthly - মাসিক বেতন'),
        ('hostel', 'Hostel - হোস্টেল ফি'),
        ('exam', 'Exam - পরীক্ষার ফি'),
        ('admission', 'Admission - ভর্তি ফি'),
        ('other', 'Other - অন্যান্য'),
    ]
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='fee_payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField()
    amount_due = models.DecimalField(max_digits=8, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_date = models.DateField()
    receipt_number = models.CharField(max_length=50, unique=True)
    note = models.CharField(max_length=255, blank=True)
    collected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    whatsapp_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def balance_due(self):
        return self.amount_due - self.amount_paid - self.discount

class FeeReminder(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
''')

create_file('apps/fees/serializers.py', '''from rest_framework import serializers
from .models import FeePayment, FeeReminder

class FeePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        fields = '__all__'

class FeeCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        fields = ['student', 'payment_type', 'month', 'year', 'amount_due', 'amount_paid', 'discount', 'payment_date', 'note']

class StudentFeeStatusSerializer(serializers.Serializer):
    monthly_fee = serializers.DecimalField(max_digits=8, decimal_places=2)
    hostel_fee = serializers.DecimalField(max_digits=8, decimal_places=2)
    paid_months = serializers.ListField()
    due_months = serializers.ListField()
    total_due = serializers.DecimalField(max_digits=10, decimal_places=2)

class FeeReportSerializer(serializers.Serializer):
    total_collected = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_due = serializers.DecimalField(max_digits=10, decimal_places=2)
''')

create_file('apps/fees/utils.py', '''import random
import datetime

def generate_receipt_number():
    year = datetime.date.today().year
    seq = f"{random.randint(1, 9999):04d}"
    return f"RCP-{year}-{seq}"

def generate_receipt_pdf(payment):
    # Mock PDF generation
    return b"PDF_CONTENT"
''')

create_file('apps/fees/views.py', '''from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import FeePayment, FeeReminder
from .serializers import FeePaymentSerializer, FeeCollectionSerializer, StudentFeeStatusSerializer, FeeReportSerializer
from .utils import generate_receipt_number, generate_receipt_pdf
from django.http import HttpResponse
from apps.notifications.whatsapp import send_fee_reminder
from apps.students.models import Student
import datetime

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
    def get(self, request, student_id):
        return Response({'status': 'mock'})

class FeeReceiptPDFView(views.APIView):
    def get(self, request, pk):
        payment = generics.get_object_or_404(FeePayment, pk=pk)
        pdf = generate_receipt_pdf(payment)
        response = HttpResponse(pdf, content_type='application/pdf')
        return response

class DueFeeListView(views.APIView):
    def get(self, request):
        return Response([])

class SendFeeReminderView(views.APIView):
    def post(self, request):
        student_id = request.data.get('student_id')
        student = Student.objects.get(id=student_id)
        send_fee_reminder(student, "January", 500)
        return Response({'status': 'sent'})

class AllStudentsFeeReportView(views.APIView):
    def get(self, request):
        return Response({'report': 'mock'})
''')

create_file('apps/fees/urls.py', '''from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.FeePaymentListView.as_view()),
    path('payments/collect/', views.FeeCollectionView.as_view()),
    path('payments/<int:pk>/receipt/', views.FeeReceiptPDFView.as_view()),
    path('students/<int:student_id>/status/', views.StudentFeeStatusView.as_view()),
    path('due/', views.DueFeeListView.as_view()),
    path('reminders/', views.SendFeeReminderView.as_view()),
    path('report/', views.AllStudentsFeeReportView.as_view()),
]
''')

# 3. Exams App
create_file('apps/exams/models.py', '''from django.db import models
from django.conf import settings
from decimal import Decimal

class Exam(models.Model):
    EXAM_TYPE = [
        ('monthly', 'Monthly Test'),
        ('midterm', 'Half Yearly - অর্ধবার্ষিক'),
        ('annual', 'Annual - বার্ষিক'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE)
    classroom = models.ForeignKey('academic.ClassRoom', on_delete=models.CASCADE)
    academic_year = models.ForeignKey('academic.AcademicYear', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ExamResult(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (80-100)'),
        ('A', 'A (70-79)'),
        ('A-', 'A- (60-69)'),
        ('B', 'B (50-59)'),
        ('C', 'C (40-49)'),
        ('D', 'D (33-39)'),
        ('F', 'F (Below 33)'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='exam_results')
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.IntegerField(default=100)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    is_absent = models.BooleanField(default=False)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['exam', 'student', 'subject']
    
    def save(self, *args, **kwargs):
        if not self.is_absent:
            pct = (self.marks_obtained / self.total_marks) * 100
            if pct >= 80: self.grade, self.gpa = 'A+', Decimal('5.00')
            elif pct >= 70: self.grade, self.gpa = 'A', Decimal('4.00')
            elif pct >= 60: self.grade, self.gpa = 'A-', Decimal('3.50')
            elif pct >= 50: self.grade, self.gpa = 'B', Decimal('3.00')
            elif pct >= 40: self.grade, self.gpa = 'C', Decimal('2.00')
            elif pct >= 33: self.grade, self.gpa = 'D', Decimal('1.00')
            else: self.grade, self.gpa = 'F', Decimal('0.00')
        super().save(*args, **kwargs)
''')

create_file('apps/exams/serializers.py', '''from rest_framework import serializers
from .models import Exam, ExamResult

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'

class BulkResultEntrySerializer(serializers.Serializer):
    results = ExamResultSerializer(many=True)

class StudentMarksheetSerializer(serializers.Serializer):
    pass

class ClassRankingSerializer(serializers.Serializer):
    pass
''')

create_file('apps/exams/utils.py', '''def generate_marksheet_pdf(student, exam, results):
    return b"PDF_CONTENT"
''')

create_file('apps/exams/views.py', '''from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import Exam, ExamResult
from .serializers import ExamSerializer, ExamResultSerializer, BulkResultEntrySerializer
from apps.notifications.whatsapp import send_result_notification
from apps.students.models import Student
from django.http import HttpResponse
from .utils import generate_marksheet_pdf

class ExamListCreateView(generics.ListCreateAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer

class ExamPublishView(views.APIView):
    def post(self, request, pk):
        exam = generics.get_object_or_404(Exam, pk=pk)
        exam.is_published = True
        exam.save()
        # Mock sending notifications
        return Response({'status': 'published'})

class ResultEntryView(views.APIView):
    def post(self, request, pk):
        return Response({'status': 'saved'})

class StudentMarksheetView(views.APIView):
    def get(self, request, student_id, exam_id):
        return Response({'status': 'mock'})

class ClassRankingView(views.APIView):
    def get(self, request, pk):
        return Response({'status': 'mock'})

class MarksheetPDFView(views.APIView):
    def get(self, request, student_id, exam_id):
        pdf = generate_marksheet_pdf(None, None, None)
        return HttpResponse(pdf, content_type='application/pdf')
''')

create_file('apps/exams/urls.py', '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.ExamListCreateView.as_view()),
    path('<int:pk>/', views.ExamDetailView.as_view()),
    path('<int:pk>/publish/', views.ExamPublishView.as_view()),
    path('<int:pk>/results/', views.ResultEntryView.as_view()),
    path('<int:pk>/ranking/', views.ClassRankingView.as_view()),
    path('students/<int:student_id>/marksheet/<int:exam_id>/', views.StudentMarksheetView.as_view()),
    path('students/<int:student_id>/marksheet/<int:exam_id>/pdf/', views.MarksheetPDFView.as_view()),
]
''')

# 4. Library App
create_file('apps/library/models.py', '''from django.db import models
from django.conf import settings
from datetime import date

class Book(models.Model):
    title = models.CharField(max_length=255)
    title_bn = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    subject_category = models.CharField(max_length=100)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

class BookIssue(models.Model):
    STATUS = [('issued','Issued'),('returned','Returned'),('overdue','Overdue')]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='issued')
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def calculate_fine(self):
        if self.status == 'issued' and date.today() > self.due_date:
            days_overdue = (date.today() - self.due_date).days
            self.fine_amount = days_overdue * 5
            self.status = 'overdue'
''')

create_file('apps/library/serializers.py', '''from rest_framework import serializers
from .models import Book, BookIssue

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BookIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = '__all__'

class BookReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookIssue
        fields = ['returned_date']
''')

create_file('apps/library/views.py', '''from rest_framework import viewsets
from .models import Book, BookIssue
from .serializers import BookSerializer, BookIssueSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookIssueViewSet(viewsets.ModelViewSet):
    queryset = BookIssue.objects.all()
    serializer_class = BookIssueSerializer
''')

create_file('apps/library/urls.py', '''from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('books', views.BookViewSet)
router.register('issues', views.BookIssueViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
''')

# 5. Notices App
create_file('apps/notices/models.py', '''from django.db import models
from django.conf import settings

class Notice(models.Model):
    TARGET_CHOICES = [
        ('all', 'All - সবাই'),
        ('guardians', 'Guardians only - অভিভাবক'),
        ('students', 'Students only - ছাত্র'),
        ('teachers', 'Teachers only - শিক্ষক'),
        ('staff', 'Staff only - কর্মী'),
    ]
    title = models.CharField(max_length=255)
    title_bn = models.CharField(max_length=255)
    body = models.TextField()
    body_bn = models.TextField()
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_sent_at = models.DateTimeField(null=True, blank=True)
    whatsapp_recipient_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
''')

create_file('apps/notices/serializers.py', '''from rest_framework import serializers
from .models import Notice

class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'

class NoticeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['title', 'title_bn', 'body', 'body_bn', 'target']
''')

create_file('apps/notices/views.py', '''from rest_framework import generics, views, status
from rest_framework.response import Response
from .models import Notice
from .serializers import NoticeSerializer, NoticeCreateSerializer
from apps.notifications.whatsapp import send_notice_broadcast
from django.utils import timezone

class NoticeListView(generics.ListAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class NoticeCreateView(generics.CreateAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeCreateSerializer

class NoticeDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

class NoticeWhatsAppBroadcastView(views.APIView):
    def post(self, request, pk):
        notice = generics.get_object_or_404(Notice, pk=pk)
        # Mock getting phones
        phones = []
        count = send_notice_broadcast(phones, notice.title, notice.body)
        notice.whatsapp_sent = True
        notice.whatsapp_sent_at = timezone.now()
        notice.whatsapp_recipient_count = count
        notice.save()
        return Response({'success_count': count})
''')

create_file('apps/notices/urls.py', '''from django.urls import path
from . import views

urlpatterns = [
    path('', views.NoticeListView.as_view()),
    path('create/', views.NoticeCreateView.as_view()),
    path('<int:pk>/', views.NoticeDetailView.as_view()),
    path('<int:pk>/broadcast/', views.NoticeWhatsAppBroadcastView.as_view()),
]
''')

# 6. Reports App
create_file('apps/reports/models.py', '')
create_file('apps/reports/serializers.py', '''from rest_framework import serializers

class DashboardStatsSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
''')
create_file('apps/reports/utils.py', '''def generate_fee_report_excel(students_data):
    pass
def generate_attendance_report_excel(data):
    pass
''')
create_file('apps/reports/views.py', '''from rest_framework import views
from rest_framework.response import Response

class DashboardStatsView(views.APIView):
    def get(self, request):
        return Response({'status': 'mock'})

class FeeReportView(views.APIView):
    def get(self, request):
        return Response({'status': 'mock'})

class AttendanceReportView(views.APIView):
    def get(self, request):
        return Response({'status': 'mock'})

class ExamResultReportView(views.APIView):
    def get(self, request):
        return Response({'status': 'mock'})
''')
create_file('apps/reports/urls.py', '''from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardStatsView.as_view()),
    path('fee-report/', views.FeeReportView.as_view()),
    path('attendance-report/', views.AttendanceReportView.as_view()),
    path('result-report/', views.ExamResultReportView.as_view()),
]
''')

print("All files generated.")
