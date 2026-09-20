from rest_framework import serializers
from .models import StudentAttendance, TeacherAttendance, HostelNightAttendance

class StudentAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentAttendance
        fields = '__all__'

class TeacherAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherAttendance
        fields = '__all__'

class HostelNightAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostelNightAttendance
        fields = '__all__'

class BulkAttendanceSerializer(serializers.Serializer):
    classroom_id = serializers.IntegerField()
    date = serializers.DateField()
    attendances = serializers.ListField(
        child=serializers.DictField() # expecting {'student_id': 1, 'status': 'present'}
    )
