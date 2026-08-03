from django.db import models
from django.contrib.auth.models import User
import datetime

class FinancialGoal(models.Model):
    GOAL_TYPES = [
        ('car', 'Buy a Car'), ('house', 'Buy a House'),
        ('emergency', 'Emergency Fund'), ('vacation', 'Vacation'),
        ('retirement', 'Retirement'), ('wedding', 'Wedding'),
        ('education', 'Education'), ('business', 'Start a Business'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=200)
    goal_type = models.CharField(max_length=20, choices=GOAL_TYPES)
    target_amount = models.DecimalField(max_digits=14, decimal_places=2)
    current_amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    deadline = models.DateField()
    
    # Advanced Forecasting Fields
    expected_inflation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=6.0, help_text="Annual inflation %")
    expected_return_rate = models.DecimalField(max_digits=5, decimal_places=2, default=10.0, help_text="Expected annual return on investments %")
    
    notes = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.goal_name} - ₹{self.target_amount}"

    def progress_percent(self):
        if self.target_amount > 0:
            return min(round((float(self.current_amount) / float(self.target_amount)) * 100, 1), 100)
        return 0

    def remaining_amount(self):
        return max(float(self.target_amount) - float(self.current_amount), 0)

    def days_remaining(self):
        delta = self.deadline - datetime.date.today()
        return max(delta.days, 0)
        
    @property
    def months_remaining(self):
        days = self.days_remaining()
        return max(days // 30, 1) # At least 1 month to avoid division by zero
        
    @property
    def required_monthly_savings(self):
        # A simplified required monthly savings without complex compound interest
        # Real implementation would use PMT formula considering expected_return_rate
        return round(self.remaining_amount() / self.months_remaining, 2)

