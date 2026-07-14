from django.db import models
from django.contrib.auth.models import User
import datetime

class Insurance(models.Model):
    INSURANCE_TYPES = [
        ('health', 'Health Insurance'), ('life', 'Life Insurance'),
        ('vehicle', 'Vehicle Insurance'), ('travel', 'Travel Insurance'),
        ('property', 'Property Insurance'), ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    policy_name = models.CharField(max_length=200)
    insurance_type = models.CharField(max_length=20, choices=INSURANCE_TYPES)
    provider = models.CharField(max_length=150)
    policy_number = models.CharField(max_length=100)
    premium_amount = models.DecimalField(max_digits=12, decimal_places=2)
    premium_frequency = models.CharField(max_length=20, choices=[
        ('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'), ('one_time', 'One Time')
    ], default='yearly')
    renewal_date = models.DateField()
    coverage_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    nominee = models.CharField(max_length=150, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.policy_name} - {self.provider}"

    def days_to_renewal(self):
        delta = self.renewal_date - datetime.date.today()
        return delta.days
