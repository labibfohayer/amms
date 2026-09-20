from django.db import models
from django.conf import settings
from decimal import Decimal

class Exam(models.Model):
    EXAM_TYPE = [
        ('monthly', 'Monthly Test'),
        ('midterm', 'Half Yearly - অর্ধবার্ষিক'),
        ('annual', 'Annual - বার্ষিক'),
        ('other', 'Other'),
    ]
    name = models.CharField(max_length=255)
    name_bn = models.CharField(max_length=255)
    exam_type = models.CharField(max_length=50, choices=EXAM_TYPE)
    classroom = models.ForeignKey('academic.ClassRoom', on_delete=models.CASCADE)
    academic_year = models.ForeignKey('academic.AcademicYear', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_published = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ExamResult(models.Model):
    GRADE_CHOICES = [
        ('A+', 'A+ (80-100)'),
        ('A', 'A (70-79)'),
        ('A-', 'A- (60-69)'),
        ('B', 'B (50-59)'),
        ('C', 'C (40-49)'),
        ('D', 'D (33-39)'),
        ('F', 'F (Below 33)'),
    ]
    
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='exam_results')
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    total_marks = models.IntegerField(default=100)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    gpa = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    is_absent = models.BooleanField(default=False)
    entered_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        unique_together = ['exam', 'student', 'subject']
    
    def save(self, *args, **kwargs):
        if not self.is_absent:
            pct = (self.marks_obtained / self.total_marks) * 100
            if pct >= 80: self.grade, self.gpa = 'A+', Decimal('5.00')
            elif pct >= 70: self.grade, self.gpa = 'A', Decimal('4.00')
            elif pct >= 60: self.grade, self.gpa = 'A-', Decimal('3.50')
            elif pct >= 50: self.grade, self.gpa = 'B', Decimal('3.00')
            elif pct >= 40: self.grade, self.gpa = 'C', Decimal('2.00')
            elif pct >= 33: self.grade, self.gpa = 'D', Decimal('1.00')
            else: self.grade, self.gpa = 'F', Decimal('0.00')
        super().save(*args, **kwargs)
