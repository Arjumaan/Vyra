from django.db import models
from django.contrib.auth.models import User
from currency.models import Currency

class TaxRecord(models.Model):
    TAX_TYPES = [
        ('income', 'Income Tax'),
        ('property', 'Property Tax'),
        ('gst', 'GST / VAT'),
        ('professional', 'Professional Tax'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tax_records')
    tax_year = models.CharField(max_length=9, help_text="e.g., 2023-2024")
    tax_type = models.CharField(max_length=20, choices=TAX_TYPES)
    
    amount_due = models.DecimalField(max_digits=14, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    filing_receipt_number = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.get_tax_type_display()} for {self.tax_year} - {self.status}"

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='donations')
    organization_name = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    
    date = models.DateField()
    is_tax_deductible = models.BooleanField(default=True, help_text="e.g., eligible for 80G deduction")
    receipt_number = models.CharField(max_length=100, blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Donation to {self.organization_name} - {self.amount}"
