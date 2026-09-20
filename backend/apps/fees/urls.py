from django.urls import path
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
