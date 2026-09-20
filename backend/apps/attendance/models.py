from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class StudentAttendance(models.Model):
    STATUS = [('present','Present'),('absent','Absent'),('late','Late'),('leave','Leave')]
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='attendance_records')
    classroom = models.ForeignKey('academic.ClassRoom', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS, default='absent')
    note = models.CharField(max_length=255, blank=True)
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    whatsapp_sent = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ['student', 'date', 'classroom']

class TeacherAttendance(models.Model):
    STATUS = [('present','Present'),('absent','Absent'),('late','Late'),('leave','Leave')]
    teacher = models.ForeignKey('teachers.Teacher', on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS)
    note = models.CharField(max_length=255, blank=True)
    
    class Meta:
        unique_together = ['teacher', 'date']

class HostelNightAttendance(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=True)
    note = models.CharField(max_length=255, blank=True)
    
    class Meta:
        unique_together = ['student', 'date']
