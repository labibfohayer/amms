from django.urls import path
from .views import (
    HostelRoomListView, HostelRoomDetailView, HostelRoomAssignView, HostelRoomUnassignView
)

urlpatterns = [
    path('', HostelRoomListView.as_view(), name='hostel-room-list'),
    path('<int:pk>/', HostelRoomDetailView.as_view(), name='hostel-room-detail'),
    path('<int:pk>/assign/', HostelRoomAssignView.as_view(), name='hostel-room-assign'),
    path('<int:pk>/unassign/', HostelRoomUnassignView.as_view(), name='hostel-room-unassign'),
]
