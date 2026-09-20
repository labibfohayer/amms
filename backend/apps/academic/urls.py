from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AcademicYearViewSet, ClassRoomViewSet, SubjectViewSet,
    TimeTableViewSet, HolidayViewSet, SyllabusViewSet
)

router = DefaultRouter()
router.register(r'academic-years', AcademicYearViewSet)
router.register(r'classrooms', ClassRoomViewSet)
router.register(r'subjects', SubjectViewSet)
router.register(r'timetables', TimeTableViewSet)
router.register(r'holidays', HolidayViewSet)
router.register(r'syllabus', SyllabusViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
