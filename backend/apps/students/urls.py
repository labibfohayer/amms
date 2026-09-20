from django.urls import path
from .views import (
    DepartmentListView, StudentListCreateView, StudentDetailView,
    StudentStatusUpdateView, StudentIDCardView
)

urlpatterns = [
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('', StudentListCreateView.as_view(), name='student_list_create'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/status/', StudentStatusUpdateView.as_view(), name='student_status_update'),
    path('<int:pk>/id-card/', StudentIDCardView.as_view(), name='student_id_card'),
]
