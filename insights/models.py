from django.db import models
from django.contrib.auth.models import User

class CashFlowForecast(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cashflow_forecasts')
    forecast_date = models.DateField()
    expected_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    ai_confidence_score = models.IntegerField(default=80, help_text="AI confidence % in this forecast")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['forecast_date']
        unique_together = ('user', 'forecast_date')

    @property
    def net_cash_flow(self):
        return self.expected_income - self.expected_expenses

    def __str__(self):
        return f"{self.user.username} - {self.forecast_date} Forecast"

class ExpenseTrend(models.Model):
    PERIOD_CHOICES = [
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expense_trends')
    category = models.CharField(max_length=100)
    trend_period = models.CharField(max_length=20, choices=PERIOD_CHOICES, default='monthly')
    
    average_spend = models.DecimalField(max_digits=12, decimal_places=2)
    predicted_spend = models.DecimalField(max_digits=12, decimal_places=2)
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'category', 'trend_period')

    def __str__(self):
        return f"{self.category} ({self.trend_period}) Trend for {self.user.username}"
