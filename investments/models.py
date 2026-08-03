from django.db import models
from django.contrib.auth.models import User
import datetime

class Investment(models.Model):
    INVESTMENT_TYPES = [
        ('mutual_fund', 'Mutual Fund'),
        ('fd', 'Fixed Deposit'),
        ('sip', 'SIP'),
        ('ppf', 'PPF'),
        ('nps', 'NPS'),
        ('gold', 'Gold'),
        ('silver', 'Silver'),
        ('real_estate', 'Real Estate'),
        ('govt_scheme', 'Government Scheme'),
        ('bond', 'Bond'),
        ('etf', 'ETF'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    investment_name = models.CharField(max_length=200)
    investment_type = models.CharField(max_length=30, choices=INVESTMENT_TYPES)
    invested_amount = models.DecimalField(max_digits=14, decimal_places=2)
    current_value = models.DecimalField(max_digits=14, decimal_places=2)
    purchase_date = models.DateField()
    broker = models.CharField(max_length=150, blank=True, null=True)
    
    # New analytics fields
    sector = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., Technology, Healthcare, Real Estate")
    risk_level = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Medium')
    
    annual_return = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    maturity_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.investment_name} ({self.get_investment_type_display()})"

    def profit_loss(self):
        return float(self.current_value) - float(self.invested_amount)

    def return_percent(self):
        if self.invested_amount > 0:
            return round((self.profit_loss() / float(self.invested_amount)) * 100, 2)
        return 0
