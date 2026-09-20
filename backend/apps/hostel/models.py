from django.db import models

class HostelRoom(models.Model):
    room_number = models.CharField(max_length=50, unique=True)
    room_number_bn = models.CharField(max_length=50)
    capacity = models.IntegerField(default=20)
    is_active = models.BooleanField(default=True)
    
    @property
    def current_occupancy(self):
        return self.students.filter(status='active').count()
    
    @property
    def available_space(self):
        return self.capacity - self.current_occupancy

    def __str__(self):
        return self.room_number
