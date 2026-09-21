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
            import uuid
            # Create user with a temporary phone first to get the auto-generated user_id
            temp_phone = f"tmp_{uuid.uuid4().hex[:10]}"
            
            # Format: DDMMYYYY
            password = validated_data.get('date_of_birth').strftime('%d%m%Y')
            
            user = User.objects.create_user(
                phone=temp_phone,
                password=password,
                name=validated_data.get('name'),
                name_bn=validated_data.get('name_bn'),
                role='student'
            )
            
            # Update phone to be the generated user_id (which acts as the login ID)
            user.phone = user.user_id
            user.save()
            
            validated_data['user'] = user
            validated_data['student_id'] = user.user_id
            validated_data['admitted_by'] = self.context['request'].user
            
            student = Student.objects.create(**validated_data)
            
            send_admission_notification(student, password)
            
            return student

class StudentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        exclude = ['user', 'student_id', 'admitted_by']
