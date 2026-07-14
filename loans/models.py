from django.db import models
from django.contrib.auth.models import User
import datetime

class Loan(models.Model):
    LOAN_TYPES = [
        ('home', 'Home Loan'), ('vehicle', 'Vehicle Loan'),
        ('education', 'Education Loan'), ('gold', 'Gold Loan'),
        ('personal', 'Personal Loan'), ('business', 'Business Loan'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    loan_name = models.CharField(max_length=200)
    loan_type = models.CharField(max_length=20, choices=LOAN_TYPES)
    lender = models.CharField(max_length=150)
    loan_amount = models.DecimalField(max_digits=14, decimal_places=2)
    outstanding_balance = models.DecimalField(max_digits=14, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    emi_amount = models.DecimalField(max_digits=12, decimal_places=2)
    emi_date = models.IntegerField(default=1, help_text="Day of month EMI is due")
    start_date = models.DateField(default=datetime.date.today)
    end_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.loan_name} ({self.get_loan_type_display()}) - {self.lender}"

    def progress_percent(self):
        if self.loan_amount > 0:
            paid = float(self.loan_amount) - float(self.outstanding_balance)
            return round((paid / float(self.loan_amount)) * 100, 1)
        return 0
