from django.db import models
from django.contrib.auth.models import User
from currency.models import Currency

class AssetCategory(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., Real Estate, Vehicles, Fine Art, Digital Assets")
    is_liquid = models.BooleanField(default=False, help_text="Can this be quickly converted to cash?")

    class Meta:
        verbose_name_plural = "Asset Categories"

    def __str__(self):
        return self.name

class Asset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assets')
    category = models.ForeignKey(AssetCategory, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=200, help_text="e.g., Primary Residence, Honda City, Rolex")
    
    # Financial details
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, blank=True)
    purchase_value = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=18, decimal_places=2, default=0)
    purchase_date = models.DateField(null=True, blank=True)
    
    # Specific details depending on the asset
    location_or_details = models.TextField(blank=True, null=True)
    
    # Tracking value over time
    last_valued_date = models.DateField(auto_now=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.current_value}"

    @property
    def appreciation(self):
        return self.current_value - self.purchase_value

class AssetValuationHistory(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='valuation_history')
    date = models.DateField()
    value = models.DecimalField(max_digits=18, decimal_places=2)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.asset.name} valued at {self.value} on {self.date}"

class RetirementPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='retirement_plan')
    current_age = models.IntegerField(default=30)
    retirement_age = models.IntegerField(default=60)
    life_expectancy = models.IntegerField(default=85)
    
    current_monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    expected_inflation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=6.0)
    expected_return_rate_pre_retirement = models.DecimalField(max_digits=5, decimal_places=2, default=10.0)
    expected_return_rate_post_retirement = models.DecimalField(max_digits=5, decimal_places=2, default=7.0)
    
    existing_retirement_corpus = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Retirement Plan for {self.user.username}"

class EmergencyFundPlan(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='emergency_fund_plan')
    months_to_cover = models.IntegerField(default=6, help_text="Number of months of expenses to save")
    current_monthly_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    current_saved_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def target_amount(self):
        return self.months_to_cover * self.current_monthly_expenses

    @property
    def remaining_amount(self):
        return max(self.target_amount - self.current_saved_amount, 0)

    def __str__(self):
        return f"Emergency Fund Plan for {self.user.username}"

