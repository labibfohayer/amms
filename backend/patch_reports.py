import os

BASE_DIR = r"C:\Users\assdi\.gemini\antigravity\scratch\amms\backend\apps"

reports_views_content = """from rest_framework import views, permissions
from rest_framework.response import Response
from django.db.models import Sum, Count, Q
from datetime import date
from decimal import Decimal
from apps.students.models import Student
from apps.attendance.models import StudentAttendance
from apps.teachers.models import Teacher
from apps.fees.models import FeePayment
from apps.notices.models import Notice
from apps.notices.serializers import NoticeSerializer
from django.http import HttpResponse
from .utils import generate_fee_report_excel
import openpyxl
from apps.exams.models import ExamResult
from django.shortcuts import get_object_or_404
from io import BytesIO

class DashboardStatsView(views.APIView):
    def get(self, request):
        today = date.today()
        current_year = today.year
        current_month = today.month

        # Student counts
        total_students = Student.objects.filter(status='active').count()
        residential = Student.objects.filter(status='active', residential_status='residential').count()
        day_scholars = total_students - residential

        # Today's attendance
        today_present = StudentAttendance.objects.filter(date=today, status='present').values('student').distinct().count()
        today_absent = StudentAttendance.objects.filter(date=today, status='absent').values('student').distinct().count()

        # Staff counts
        total_teachers = Teacher.objects.filter(is_active=True, staff_type='teacher').count()
        total_staff = Teacher.objects.filter(is_active=True).exclude(staff_type='teacher').count()

        # Fee dues
        all_active_students = Student.objects.filter(status='active').select_related()
        total_due = Decimal('0')
        for s in all_active_students:
            months_elapsed = current_month
            expected = s.monthly_fee * months_elapsed
            paid = FeePayment.objects.filter(student=s, payment_type='monthly', year=current_year).aggregate(total=Sum('amount_paid'))['total'] or Decimal('0')
            due = expected - paid
            if due > 0:
                total_due += due

        # Latest notices (5)
        latest_notices = Notice.objects.filter(is_active=True).order_by('-created_at')[:5]

        # Department-wise counts
        dept_counts = Student.objects.filter(status='active').values('islamic_department__name', 'general_department__name').annotate(count=Count('id'))

        return Response({
            "total_students": total_students,
            "residential_students": residential,
            "day_students": day_scholars,
            "today_present": today_present,
            "today_absent": today_absent,
            "total_teachers": total_teachers,
            "total_staff": total_staff,
            "total_due_fee": str(total_due),
            "latest_notices": NoticeSerializer(latest_notices, many=True).data,
            "department_counts": list(dept_counts)
        })

class FeeReportView(views.APIView):
    def get(self, request):
        students_data = []
        payments = FeePayment.objects.all()
        # simplified data aggregation for the report to demonstrate functionality
        for p in payments:
            students_data.append({
                'name': getattr(p.student, 'name', 'N/A') if p.student else 'N/A',
                'class_name': 'N/A',
                'monthly_fee': p.amount_due,
                'months_paid': 1,
                'total_paid': p.amount_paid,
                'total_due': p.balance_due
            })
        excel_bytes = generate_fee_report_excel(students_data)
        response = HttpResponse(excel_bytes, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="fee_report.xlsx"'
        return response

class AttendanceReportView(views.APIView):
    def get(self, request):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        classroom_id = request.query_params.get('classroom_id')
        
        if not all([month, year, classroom_id]):
            return Response({"error": "Missing parameters"}, status=400)
            
        attendances = StudentAttendance.objects.filter(
            date__month=month,
            date__year=year,
            classroom_id=classroom_id
        ).select_related('student')
        
        student_stats = {}
        for att in attendances:
            student = att.student
            if student.id not in student_stats:
                class_name = student.islamic_department.name if student.islamic_department else (student.general_department.name if student.general_department else '')
                student_stats[student.id] = {
                    'roll': student.roll_number,
                    'name': student.name,
                    'class': class_name,
                    'present': 0,
                    'absent': 0,
                    'late': 0
                }
            
            if att.status == 'present':
                student_stats[student.id]['present'] += 1
            elif att.status == 'absent':
                student_stats[student.id]['absent'] += 1
            elif att.status == 'late':
                student_stats[student.id]['late'] += 1
                
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Attendance Report"
        
        headers = ["Roll", "Name", "Class", "Present Days", "Absent Days", "Late Days", "Attendance %"]
        ws.append(headers)
        
        sorted_students = sorted(student_stats.values(), key=lambda x: (x['roll'] or 0))
        
        tot_present = 0
        tot_absent = 0
        tot_late = 0
        
        for st in sorted_students:
            total_days = st['present'] + st['absent'] + st['late']
            pct = (st['present'] / total_days * 100) if total_days > 0 else 0
            ws.append([
                st['roll'],
                st['name'],
                st['class'],
                st['present'],
                st['absent'],
                st['late'],
                f"{pct:.2f}%"
            ])
            tot_present += st['present']
            tot_absent += st['absent']
            tot_late += st['late']
            
        ws.append(["Totals", "", "", tot_present, tot_absent, tot_late, ""])
        
        buffer = BytesIO()
        wb.save(buffer)
        
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        month_name = date(int(year), int(month), 1).strftime('%b')
        response['Content-Disposition'] = f'attachment; filename="attendance_report_{month_name}_{year}.xlsx"'
        return response

class ExamResultReportView(views.APIView):
    def get(self, request):
        exam_id = request.query_params.get('exam_id')
        if not exam_id:
            return Response({"error": "Missing exam_id"}, status=400)
            
        results = ExamResult.objects.filter(exam_id=exam_id).select_related('student', 'subject')
        
        student_data = {}
        subjects = set()
        
        for r in results:
            student = r.student
            subjects.add(r.subject.name)
            
            if student.id not in student_data:
                student_data[student.id] = {
                    'roll': student.roll_number,
                    'name': student.name,
                    'subjects': {},
                    'total': 0,
                    'gpas': []
                }
            
            student_data[student.id]['subjects'][r.subject.name] = r.marks_obtained
            student_data[student.id]['total'] += r.marks_obtained
            if r.gpa is not None:
                student_data[student.id]['gpas'].append(r.gpa)
                
        # Calculate rank and GPA
        students_list = list(student_data.values())
        students_list.sort(key=lambda x: x['total'], reverse=True)
        
        current_rank = 1
        for i in range(len(students_list)):
            if i > 0 and students_list[i]['total'] < students_list[i-1]['total']:
                current_rank = i + 1
            students_list[i]['rank'] = current_rank
            
            gpas = students_list[i]['gpas']
            students_list[i]['avg_gpa'] = sum(gpas)/len(gpas) if gpas else 0
            
            # Simple grade calculation based on GPA
            avg_gpa = students_list[i]['avg_gpa']
            if avg_gpa >= 5.0: grade = 'A+'
            elif avg_gpa >= 4.0: grade = 'A'
            elif avg_gpa >= 3.5: grade = 'A-'
            elif avg_gpa >= 3.0: grade = 'B'
            elif avg_gpa >= 2.0: grade = 'C'
            elif avg_gpa >= 1.0: grade = 'D'
            else: grade = 'F'
            students_list[i]['grade'] = grade
            
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Exam Results"
        
        subject_list = sorted(list(subjects))
        headers = ["Rank", "Roll", "Name"] + subject_list + ["Total", "GPA", "Grade"]
        ws.append(headers)
        
        for st in students_list:
            row = [st['rank'], st['roll'], st['name']]
            for sub in subject_list:
                row.append(st['subjects'].get(sub, ''))
            row.extend([st['total'], f"{st['avg_gpa']:.2f}", st['grade']])
            ws.append(row)
            
        buffer = BytesIO()
        wb.save(buffer)
        
        response = HttpResponse(buffer.getvalue(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="exam_result_report.xlsx"'
        return response
"""

with open(os.path.join(BASE_DIR, 'reports', 'views.py'), 'w', encoding='utf-8') as f:
    f.write(reports_views_content)

print("Patched reports/views.py")
