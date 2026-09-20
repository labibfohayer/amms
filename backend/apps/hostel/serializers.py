from rest_framework import serializers
from .models import HostelRoom
from apps.students.models import Student

class StudentBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'student_id', 'name', 'name_bn', 'phone'] # assuming phone in Student? It has guardian_phone
        # Let's adjust fields:
        # fields = ['id', 'student_id', 'name', 'name_bn', 'guardian_phone']

class HostelRoomSerializer(serializers.ModelSerializer):
    current_occupancy = serializers.ReadOnlyField()
    available_space = serializers.ReadOnlyField()

    class Meta:
        model = HostelRoom
        fields = ['id', 'room_number', 'room_number_bn', 'capacity', 'is_active', 'current_occupancy', 'available_space']

class HostelRoomDetailSerializer(serializers.ModelSerializer):
    current_occupancy = serializers.ReadOnlyField()
    available_space = serializers.ReadOnlyField()
    students = serializers.SerializerMethodField()

    class Meta:
        model = HostelRoom
        fields = ['id', 'room_number', 'room_number_bn', 'capacity', 'is_active', 'current_occupancy', 'available_space', 'students']

    def get_students(self, obj):
        active_students = obj.students.filter(status='active')
        return [{"id": s.id, "student_id": s.student_id, "name": s.name} for s in active_students]
