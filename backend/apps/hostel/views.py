from rest_framework import generics, views, status, permissions
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import HostelRoom
from .serializers import HostelRoomSerializer, HostelRoomDetailSerializer
from apps.students.models import Student

class IsPrincipalOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['principal', 'vice_principal', 'managing_director', 'teacher']

class HostelRoomListView(generics.ListAPIView):
    queryset = HostelRoom.objects.all()
    serializer_class = HostelRoomSerializer
    permission_classes = [IsPrincipalOrTeacher]

class HostelRoomDetailView(generics.RetrieveAPIView):
    queryset = HostelRoom.objects.all()
    serializer_class = HostelRoomDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

class HostelRoomAssignView(views.APIView):
    permission_classes = [IsPrincipalOrTeacher]
    
    def post(self, request, pk):
        room = get_object_or_404(HostelRoom, pk=pk)
        student_id = request.data.get('student_id')
        student = get_object_or_404(Student, pk=student_id)
        
        if room.available_space > 0:
            student.hostel_room = room
            student.save()
            return Response({'status': 'Student assigned to room successfully'})
        return Response({'error': 'Room is full'}, status=status.HTTP_400_BAD_REQUEST)

class HostelRoomUnassignView(views.APIView):
    permission_classes = [IsPrincipalOrTeacher]
    
    def post(self, request, pk):
        room = get_object_or_404(HostelRoom, pk=pk)
        student_id = request.data.get('student_id')
        student = get_object_or_404(Student, pk=student_id)
        
        if student.hostel_room == room:
            student.hostel_room = None
            student.save()
            return Response({'status': 'Student removed from room'})
        return Response({'error': 'Student not in this room'}, status=status.HTTP_400_BAD_REQUEST)
