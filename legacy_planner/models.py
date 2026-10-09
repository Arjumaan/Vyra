from django.db import models
from django.contrib.auth.models import User

class TrustedContact(models.Model):
    ACCESS_ROLES = [
        ('VIEW', 'View Only'),
        ('EMERGENCY', 'Emergency Access'),
        ('LEGACY', 'Legacy Executor'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trusted_contacts')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    relationship = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ACCESS_ROLES, default='VIEW')
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.get_role_display()})"

class Beneficiary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beneficiaries')
    name = models.CharField(max_length=200)
    relationship = models.CharField(max_length=100)
    allocation_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    notes = models.TextField(blank=True, null=True, help_text="Specific assets or instructions (Not legally binding)")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.allocation_percentage}%"

class DeadMansSwitch(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Active (Monitoring)'),
        ('WARNING', 'Warning (Verification Pending)'),
        ('TRIGGERED', 'Triggered (Releasing Data)'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='dead_mans_switch')
    is_enabled = models.BooleanField(default=False)
    
    # Configuration
    check_in_frequency_days = models.IntegerField(default=30)
    grace_period_days = models.IntegerField(default=14)
    
    # State tracking
    last_check_in = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    # Security
    cryptographic_key_hash = models.CharField(max_length=256, blank=True, null=True)
    
    def __str__(self):
        return f"Switch for {self.user.username} - {self.status}"
