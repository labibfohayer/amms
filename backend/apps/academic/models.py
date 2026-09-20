from django.db import models
from apps.students.models import Department

class AcademicYear(models.Model):
    year = models.IntegerField(unique=True)
    is_current = models.BooleanField(default=False)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.year)

class ClassRoom(models.Model):
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    section = models.CharField(max_length=5, default='A')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey('teachers.Teacher', null=True, blank=True, on_delete=models.SET_NULL)
    capacity = models.IntegerField(default=50)
    
    class Meta:
        unique_together = ['department', 'section', 'academic_year']

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey('teachers.Teacher', null=True, blank=True, on_delete=models.SET_NULL)
    total_marks = models.IntegerField(default=100)
    pass_marks = models.IntegerField(default=33)
    is_optional = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.code})"

class TimeTable(models.Model):
    DAYS = [('sat','Saturday'),('sun','Sunday'),('mon','Monday'),('tue','Tuesday'),('wed','Wednesday'),('thu','Thursday')]
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey('teachers.Teacher', null=True, on_delete=models.SET_NULL)
    day = models.CharField(max_length=10, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

class Holiday(models.Model):
    date = models.DateField(unique=True)
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)

class Syllabus(models.Model):
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='syllabus/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
