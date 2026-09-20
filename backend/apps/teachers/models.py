from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Teacher(models.Model):
    STAFF_TYPE = [
        ('teacher', 'শিক্ষক - Teacher'),
        ('staff', 'কর্মী - Staff'),
        ('accountant', 'হিসাবরক্ষক - Accountant'),
        ('other', 'অন্যান্য - Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='teachers/photos/', null=True, blank=True)
    staff_type = models.CharField(max_length=20, choices=STAFF_TYPE)
    designation = models.CharField(max_length=255)
    designation_bn = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    joining_date = models.DateField()
    monthly_salary = models.DecimalField(max_digits=8, decimal_places=2)
    address = models.TextField()
    nid = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='added_teachers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.teacher_id})"

class SalaryPayment(models.Model):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='salary_payments')
    month = models.IntegerField()
    year = models.IntegerField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    paid_date = models.DateField()
    note = models.TextField(blank=True)
    paid_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['teacher', 'month', 'year']

    def __str__(self):
        return f"{self.teacher.name} - {self.month}/{self.year}"

class LeaveApplication(models.Model):
    STATUS = [('pending','Pending'),('approved','Approved'),('rejected','Rejected')]
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    leave_type = models.CharField(max_length=50)
    from_date = models.DateField()
    to_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default='pending')
    reviewed_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.name} - {self.leave_type}"
