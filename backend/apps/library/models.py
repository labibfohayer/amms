from django.db import models
from django.conf import settings
from datetime import date

class Book(models.Model):
    title = models.CharField(max_length=255)
    title_bn = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    subject_category = models.CharField(max_length=100)
    isbn = models.CharField(max_length=50, blank=True, null=True)
    total_copies = models.IntegerField(default=1)
    available_copies = models.IntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

class BookIssue(models.Model):
    STATUS = [('issued','Issued'),('returned','Returned'),('overdue','Overdue')]
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    student = models.ForeignKey('students.Student', on_delete=models.CASCADE)
    issued_date = models.DateField(auto_now_add=True)
    due_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default='issued')
    fine_amount = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    issued_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    
    def calculate_fine(self):
        if self.status == 'issued' and date.today() > self.due_date:
            days_overdue = (date.today() - self.due_date).days
            self.fine_amount = days_overdue * 5
            self.status = 'overdue'
