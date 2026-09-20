from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Department(models.Model):
    name = models.CharField(max_length=255)
    name_en = models.CharField(max_length=255)
    dept_type = models.CharField(max_length=20, choices=[('islamic', 'Islamic'), ('general', 'General')])
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return f"{self.name_en} ({self.name})"

class Student(models.Model):
    ENROLLMENT_TYPE = [
        ('islamic_only', 'Islamic Only'),
        ('general_only', 'General Only'),
        ('both', 'Both'),
    ]
    RESIDENTIAL_STATUS = [
        ('residential', 'Residential - আবাসিক'),
        ('day', 'Day Scholar - অনাবাসিক'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('expelled', 'Expelled'),
        ('passed_out', 'Passed Out'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=50, unique=True)
    
    # Personal info
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    father_name = models.CharField(max_length=255)
    father_name_bn = models.CharField(max_length=255)
    mother_name = models.CharField(max_length=255)
    mother_name_bn = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    birth_reg_no = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to='students/photos/', null=True, blank=True)
    
    # Address
    present_address = models.TextField()
    permanent_address = models.TextField()
    
    # Guardian info
    guardian_name = models.CharField(max_length=255)
    guardian_relationship = models.CharField(max_length=50)
    guardian_phone = models.CharField(max_length=20)
    guardian_nid = models.CharField(max_length=50, blank=True)
    
    # Academic
    enrollment_type = models.CharField(max_length=20, choices=ENROLLMENT_TYPE)
    islamic_department = models.ForeignKey(Department, null=True, blank=True, related_name='islamic_students', on_delete=models.SET_NULL)
    general_department = models.ForeignKey(Department, null=True, blank=True, related_name='general_students', on_delete=models.SET_NULL)
    section = models.CharField(max_length=5, default='A')
    roll_number = models.IntegerField(null=True, blank=True)
    admission_date = models.DateField()
    academic_year = models.IntegerField()
    previous_institution = models.CharField(max_length=255, blank=True)
    
    # Residential
    residential_status = models.CharField(max_length=20, choices=RESIDENTIAL_STATUS)
    hostel_room = models.ForeignKey('hostel.HostelRoom', on_delete=models.SET_NULL, null=True, blank=True, related_name='students')
    
    # Fee
    monthly_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    hostel_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    expulsion_reason = models.TextField(blank=True)
    
    admitted_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admitted_students')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.student_id}"
