from rest_framework import serializers
from .models import FeePayment, FeeReminder

class FeePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        fields = '__all__'

class FeeCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeePayment
        fields = ['student', 'payment_type', 'month', 'year', 'amount_due', 'amount_paid', 'discount', 'payment_date', 'note']

class StudentFeeStatusSerializer(serializers.Serializer):
    monthly_fee = serializers.DecimalField(max_digits=8, decimal_places=2)
    hostel_fee = serializers.DecimalField(max_digits=8, decimal_places=2)
    paid_months = serializers.ListField()
    due_months = serializers.ListField()
    total_due = serializers.DecimalField(max_digits=10, decimal_places=2)

class FeeReportSerializer(serializers.Serializer):
    total_collected = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_due = serializers.DecimalField(max_digits=10, decimal_places=2)
