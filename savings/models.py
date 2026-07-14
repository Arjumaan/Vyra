from django.db import models
from django.contrib.auth.models import User
import datetime

class SavingsAccount(models.Model):
    ACCOUNT_TYPES = [
        ('savings', 'Savings Account'),
        ('fd', 'Fixed Deposit'),
        ('rd', 'Recurring Deposit'),
        ('ppf', 'PPF'),
        ('nps', 'NPS'),
        ('emergency', 'Emergency Fund'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=150)
    bank = models.CharField(max_length=150)
    account_type = models.CharField(max_length=30, choices=ACCOUNT_TYPES, default='savings')
    current_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    monthly_contribution = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    goal_amount = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    goal_deadline = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account_name} - {self.bank}"

    def progress_percent(self):
        if self.goal_amount and self.goal_amount > 0:
            return min(round((float(self.current_balance) / float(self.goal_amount)) * 100, 1), 100)
        return 0

class SavingsTransaction(models.Model):
    TRANSACTION_TYPES = [('deposit', 'Deposit'), ('withdrawal', 'Withdrawal')]
    account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=datetime.date.today)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.amount}"
