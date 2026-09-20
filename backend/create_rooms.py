import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.hostel.models import HostelRoom
rooms = [
    ('Room 1', 'রুম ১'), ('Room 2', 'রুম ২'),
    ('Room 3', 'রুম ৩'), ('Room 4', 'রুম ৪'),
]
for num, bn in rooms:
    HostelRoom.objects.get_or_create(room_number=num, defaults={'room_number_bn': bn})
    
print("Rooms created.")
