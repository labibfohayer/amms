from rest_framework import serializers
from .models import Exam, ExamResult

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'

class BulkResultEntrySerializer(serializers.Serializer):
    results = ExamResultSerializer(many=True)

class StudentMarksheetSerializer(serializers.Serializer):
    pass

class ClassRankingSerializer(serializers.Serializer):
    pass
