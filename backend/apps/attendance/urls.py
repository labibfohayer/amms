from django.urls import path
from .views import (
    StudentAttendanceBulkView, StudentAttendanceListView, StudentAttendanceMonthlyView,
    TeacherAttendanceBulkView, HostelAttendanceView, AttendanceReportView
)

urlpatterns = [
    path('students/bulk/', StudentAttendanceBulkView.as_view(), name='student-attendance-bulk'),
    path('students/', StudentAttendanceListView.as_view(), name='student-attendance-list'),
    path('students/<int:student_id>/monthly/<int:month>/<int:year>/', StudentAttendanceMonthlyView.as_view(), name='student-attendance-monthly'),
    path('teachers/bulk/', TeacherAttendanceBulkView.as_view(), name='teacher-attendance-bulk'),
    path('hostel/', HostelAttendanceView.as_view(), name='hostel-attendance'),
    path('report/', AttendanceReportView.as_view(), name='attendance-report'),
]
