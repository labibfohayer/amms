from django.db import models
from django.conf import settings

class Notice(models.Model):
    TARGET_CHOICES = [
        ('all', 'All - সবাই'),
        ('guardians', 'Guardians only - অভিভাবক'),
        ('students', 'Students only - ছাত্র'),
        ('teachers', 'Teachers only - শিক্ষক'),
        ('staff', 'Staff only - কর্মী'),
    ]
    title = models.CharField(max_length=255)
    title_bn = models.CharField(max_length=255)
    body = models.TextField()
    body_bn = models.TextField()
    target = models.CharField(max_length=20, choices=TARGET_CHOICES, default='all')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)
    whatsapp_sent = models.BooleanField(default=False)
    whatsapp_sent_at = models.DateTimeField(null=True, blank=True)
    whatsapp_recipient_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
