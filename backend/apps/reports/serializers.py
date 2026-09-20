from rest_framework import serializers

class DashboardStatsSerializer(serializers.Serializer):
    total_students = serializers.IntegerField()
