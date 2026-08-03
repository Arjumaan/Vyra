from django.db import models
from django.contrib.auth.models import User

class AIFinancialCoachSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_sessions')
    started_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"AI Session for {self.user.username} starting {self.started_at}"

class AIMessage(models.Model):
    SENDER_CHOICES = [
        ('user', 'User'),
        ('ai', 'AI Coach'),
    ]

    session = models.ForeignKey(AIFinancialCoachSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} at {self.timestamp}"

class AIMonthlyReport(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_monthly_reports')
    month = models.IntegerField()
    year = models.IntegerField()
    
    summary_text = models.TextField()
    alerts_data = models.JSONField(default=list, help_text="List of warnings or critical alerts")
    strategies_data = models.JSONField(default=list, help_text="List of AI suggested strategies")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'month', 'year')

    def __str__(self):
        return f"AI Report {self.month}/{self.year} for {self.user.username}"
