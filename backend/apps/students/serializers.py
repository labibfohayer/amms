from rest_framework import serializers
from .models import Department, Student
from django.contrib.auth import get_user_model
from django.db import transaction
import datetime
from apps.notifications.whatsapp import send_admission_notification

User = get_user_model()

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class StudentListSerializer(serializers.ModelSerializer):
    islamic_department_name = serializers.CharField(source='islamic_department.name_en', read_only=True)
    general_department_name = serializers.CharField(source='general_department.name_en', read_only=True)

    class Meta:
        model = Student
        fields = ['id', 'student_id', 'name', 'islamic_department_name', 'general_department_name', 'roll_number', 'status', 'photo']

class StudentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudentAdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['user', 'student_id', 'admitted_by']
        
    def create(self, validated_data):
        with transaction.atomic():
            phone = validated_data.get('guardian_phone')
            base_phone = phone
            counter = 1
            while User.objects.filter(phone=phone).exists():
                phone = f"{base_phone}_{counter}"
                counter += 1

            user = User.objects.create_user(
                phone=phone,
                password=validated_data.get('date_of_birth').strftime('%Y%m%d'),
                name=validated_data.get('name'),
                name_bn=validated_data.get('name_bn'),
                role='student'
            )
            
            validated_data['user'] = user
            validated_data['student_id'] = user.user_id
            validated_data['admitted_by'] = self.context['request'].user
            
            student = Student.objects.create(**validated_data)
            
            password = validated_data.get('date_of_birth').strftime('%Y%m%d')
            send_admission_notification(student, password)
            
            return student

class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['user', 'student_id', 'admitted_by']
