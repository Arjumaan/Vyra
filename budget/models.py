from django.db import models
from django.contrib.auth.models import User
import datetime

class Budget(models.Model):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    BUDGET_TYPES = [
        ('monthly', 'Monthly Fixed'),
        ('daily', 'Daily Allocation'),
        ('rolling', 'Rolling/Carryover'),
        ('department', 'Department/Project'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    budget_type = models.CharField(max_length=20, choices=BUDGET_TYPES, default='monthly')
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2, help_text="Total overarching budget")
    month = models.IntegerField(choices=MONTH_CHOICES, default=datetime.datetime.now().month)
    year = models.IntegerField(default=datetime.datetime.now().year)
    
    # Advanced tracking
    department_name = models.CharField(max_length=100, blank=True, null=True, help_text="Used only for department budgets")
    is_ai_generated = models.BooleanField(default=False, help_text="Was this budget baseline suggested by AI?")
    carryover_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, help_text="Amount carried over from previous period")

    class Meta:
        unique_together = ('user', 'month', 'year')

    def __str__(self):
        return f"{self.user.username} - {self.get_month_display()} {self.year} - {self.monthly_budget}"

class CategoryBudget(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name='category_budgets')
    category_name = models.CharField(max_length=100)
    allocated_amount = models.DecimalField(max_digits=12, decimal_places=2)
    is_ai_generated = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.category_name} - {self.allocated_amount} ({self.budget.get_month_display()})"
