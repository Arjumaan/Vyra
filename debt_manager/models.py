from django.db import models
from django.contrib.auth.models import User

class Debt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='debts')
    name = models.CharField(max_length=150)
    principal_balance = models.DecimalField(max_digits=14, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, help_text="Annual Percentage Rate (APR)")
    minimum_payment = models.DecimalField(max_digits=14, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - ₹{self.principal_balance}"

class DebtStrategy(models.Model):
    STRATEGY_CHOICES = [
        ('snowball', 'Debt Snowball (Lowest Balance First)'),
        ('avalanche', 'Debt Avalanche (Highest Interest First)'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='debt_strategy')
    strategy_type = models.CharField(max_length=20, choices=STRATEGY_CHOICES, default='avalanche')
    extra_monthly_payment = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    
    def __str__(self):
        return f"{self.user.username}'s Strategy: {self.get_strategy_type_display()}"
