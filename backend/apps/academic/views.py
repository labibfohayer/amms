from rest_framework import viewsets, permissions
from .models import AcademicYear, ClassRoom, Subject, TimeTable, Holiday, Syllabus
from .serializers import (
    AcademicYearSerializer, ClassRoomSerializer, SubjectSerializer,
    TimeTableSerializer, HolidaySerializer, SyllabusSerializer
)

class IsPrincipalOrTeacher(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role in ['principal', 'vice_principal', 'managing_director', 'teacher']

class AcademicYearViewSet(viewsets.ModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsPrincipalOrTeacher]

class ClassRoomViewSet(viewsets.ModelViewSet):
    queryset = ClassRoom.objects.all()
    serializer_class = ClassRoomSerializer
    permission_classes = [IsPrincipalOrTeacher]

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsPrincipalOrTeacher]

class TimeTableViewSet(viewsets.ModelViewSet):
    queryset = TimeTable.objects.all()
    serializer_class = TimeTableSerializer
    permission_classes = [IsPrincipalOrTeacher]

class HolidayViewSet(viewsets.ModelViewSet):
    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    permission_classes = [IsPrincipalOrTeacher]

class SyllabusViewSet(viewsets.ModelViewSet):
    queryset = Syllabus.objects.all()
    serializer_class = SyllabusSerializer
    permission_classes = [IsPrincipalOrTeacher]
