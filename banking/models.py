from django.db import models
from django.contrib.auth.models import User

class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('savings', 'Savings'), ('current', 'Current'),
        ('salary', 'Salary'), ('nri', 'NRI'), ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=150)
    account_number = models.CharField(max_length=20)  # stored masked
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='savings')
    branch = models.CharField(max_length=150, blank=True, null=True)
    ifsc = models.CharField(max_length=20, blank=True, null=True)
    current_balance = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank_name} (...{self.account_number[-4:] if len(self.account_number) >= 4 else self.account_number})"

class CreditCard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank = models.CharField(max_length=150)
    card_name = models.CharField(max_length=150)
    credit_limit = models.DecimalField(max_digits=12, decimal_places=2)
    used_credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    due_date = models.DateField()
    billing_cycle_day = models.IntegerField(default=1)
    minimum_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    annual_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_name} - {self.bank}"

    def available_credit(self):
        return float(self.credit_limit) - float(self.used_credit)

    def utilization_percent(self):
        if self.credit_limit > 0:
            return round((float(self.used_credit) / float(self.credit_limit)) * 100, 1)
        return 0
