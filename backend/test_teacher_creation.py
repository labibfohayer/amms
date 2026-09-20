import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.teachers.serializers import TeacherCreateSerializer
from rest_framework.request import Request
from django.test import RequestFactory
from django.contrib.auth import get_user_model

User = get_user_model()
admin = User.objects.get(phone='01700000000')

factory = RequestFactory()
req = factory.post('/')
req.user = admin
request = Request(req)

data = {
    'name': 'Test Teacher',
    'phone': '01900000000',
    'staff_type': 'teacher',
    'designation': 'Asst Teacher',
    'designation_bn': 'সহকারী শিক্ষক',
    'qualification': 'MSc',
    'joining_date': '2026-01-01',
    'monthly_salary': 15000,
    'address': 'Dhaka'
}

serializer = TeacherCreateSerializer(data=data, context={'request': request})
if serializer.is_valid():
    teacher = serializer.save()
    print('Teacher created:', teacher.teacher_id)
else:
    print('Errors:', serializer.errors)
