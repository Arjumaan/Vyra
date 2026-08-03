from django.db import models
from django.contrib.auth.models import User
from currency.models import Currency

class Subscription(models.Model):
    CYCLE_CHOICES = [
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('paused', 'Paused'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    service_name = models.CharField(max_length=150, help_text="e.g., Netflix, Spotify, AWS")
    plan_name = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Premium Family")
    billing_cycle = models.CharField(max_length=20, choices=CYCLE_CHOICES, default='monthly')
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    
    start_date = models.DateField()
    next_billing_date = models.DateField()
    
    auto_renew = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['next_billing_date']

    def __str__(self):
        return f"{self.service_name} - {self.amount}/{self.billing_cycle}"
