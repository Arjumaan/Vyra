from django.db import models
from django.contrib.auth.models import User

class DatabaseBackup(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    ]

    backup_file = models.FileField(upload_to='backups/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_encrypted = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Backup {self.created_at.strftime('%Y-%m-%d %H:%M:%S')} - {self.status}"

class SecurityLog(models.Model):
    ACTION_CHOICES = [
        ('login_success', 'Login Success'),
        ('login_failed', 'Login Failed'),
        ('password_change', 'Password Changed'),
        ('data_export', 'Data Exported'),
        ('backup_created', 'Backup Created'),
        ('suspicious_activity', 'Suspicious Activity Detected'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='security_logs')
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        user_str = self.user.username if self.user else "Unknown User"
        return f"[{self.action}] {user_str} at {self.timestamp}"
