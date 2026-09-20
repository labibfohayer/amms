from django.db import models
from django.conf import settings

class FeePayment(models.Model):
    PAYMENT_STATUS = [
        ('paid', 'Paid - পরিশোধিত'),
        ('partial', 'Partial - আংশিক'),
    ]
    PAYMENT_TYPE = [
        ('monthly', 'Monthly - মাসিক বেতন'),
        ('hostel', 'Hostel - হোস্টেল ফি'),
        ('exam', 'Exam - পরীক্ষার ফি'),
        ('admission', 'Admission - ভর্তি ফি'),
        ('other', 'Other - অন্যান্য'),
    ]
    
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE, related_name='fee_payments')
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE)
    month = models.IntegerField(null=True, blank=True)
    year = models.IntegerField()
    amount_due = models.DecimalField(max_digits=8, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    payment_date = models.DateField()
    receipt_number = models.CharField(max_length=50, unique=True)
    note = models.CharField(max_length=255, blank=True)
    collected_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    whatsapp_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    @property
    def balance_due(self):
        return self.amount_due - self.amount_paid - self.discount

class FeeReminder(models.Model):
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    sent_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
