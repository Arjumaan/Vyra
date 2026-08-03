from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from currency.models import Currency

class UserSettings(models.Model):
    THEME_CHOICES = [
        ('light', 'Light Mode (Neumorphic)'),
        ('dark', 'Dark Mode'),
        ('system', 'System Default'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='platform_settings')
    theme = models.CharField(max_length=20, choices=THEME_CHOICES, default='light')
    
    # Financial preferences
    base_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True, help_text="Override system base currency for this user")
    
    # Notification preferences
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=False)
    budget_alerts = models.BooleanField(default=True)
    bill_reminders = models.BooleanField(default=True)
    investment_alerts = models.BooleanField(default=True)
    security_alerts = models.BooleanField(default=True)
    
    # Privacy
    hide_balances_by_default = models.BooleanField(default=False)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Settings"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('budget', 'Budget Alert'),
        ('bill', 'Bill Reminder'),
        ('investment', 'Investment Alert'),
        ('security', 'Security Alert'),
        ('system', 'System Message'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='system')
    title = models.CharField(max_length=150)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_notification_type_display()}] {self.title}"

# Signal to auto-create UserSettings when User is created
@receiver(post_save, sender=User)
def create_user_settings(sender, instance, created, **kwargs):
    if created:
        UserSettings.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_settings(sender, instance, **kwargs):
    instance.platform_settings.save()
