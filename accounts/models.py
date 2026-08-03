from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class FinancialProfile(models.Model):
    RISK_CHOICES = [
        ('Low', 'Low Risk - Capital Preservation'),
        ('Medium', 'Medium Risk - Balanced Growth'),
        ('High', 'High Risk - Aggressive Growth'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('Beginner', 'Beginner (< 2 years)'),
        ('Intermediate', 'Intermediate (2-5 years)'),
        ('Expert', 'Expert (5+ years)'),
    ]

    # Core Identity
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='financial_profile')
    
    # Career & Income
    occupation = models.CharField(max_length=100, blank=True, null=True)
    employer = models.CharField(max_length=100, blank=True, null=True)
    monthly_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    annual_salary = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    other_income_sources = models.TextField(blank=True, null=True, help_text="List other income sources (e.g., Freelancing, Rental)")
    
    # Localization
    country = models.CharField(max_length=100, blank=True, null=True, default="India")
    state = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, default='INR', help_text="Base currency for reports")
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    
    # Investment Profile
    risk_appetite = models.CharField(max_length=20, choices=RISK_CHOICES, default='Medium')
    investment_experience = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='Beginner')
    preferred_investment_types = models.TextField(blank=True, null=True, help_text="e.g., Stocks, Mutual Funds, Real Estate")
    preferred_banks = models.TextField(blank=True, null=True, help_text="Preferred banking partners")
    
    # Life Goals & Dependents
    retirement_age = models.IntegerField(default=60)
    number_of_dependents = models.IntegerField(default=0)
    financial_goals = models.TextField(blank=True, null=True, help_text="High-level goals (e.g., Buy a house, Retire early)")
    monthly_savings_target = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    emergency_fund_target = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    
    # Vault & KYC (Sensitive info should ideally be encrypted, masked in UI)
    pan_number = models.CharField(max_length=20, blank=True, null=True)
    aadhaar_number = models.CharField(max_length=20, blank=True, null=True)
    nominee_name = models.CharField(max_length=100, blank=True, null=True)
    nominee_relation = models.CharField(max_length=50, blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Financial Profile"

    def get_masked_aadhaar(self):
        if self.aadhaar_number and len(self.aadhaar_number) >= 4:
            return f"********{self.aadhaar_number[-4:]}"
        return ""

# Signal to auto-create FinancialProfile when User is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        FinancialProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.financial_profile.save()
