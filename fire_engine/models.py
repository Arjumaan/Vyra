from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class FIREProfile(models.Model):
    """
    Core profile holding assumptions and goals for a user's Financial Independence, Retire Early (FIRE) plan.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fire_profile')
    
    # Financial Assumptions (using Decimal for precise financial math)
    safe_withdrawal_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('4.00'), help_text="e.g., 4.00 for 4% rule")
    expected_investment_return = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('7.00'), help_text="Real return after inflation, e.g., 7.00 for 7%")
    inflation_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('3.00'), help_text="e.g., 3.00 for 3%")
    
    # Goals
    current_age = models.IntegerField(default=30)
    target_retirement_age = models.IntegerField(default=50)
    
    # Manual overrides (In a full OS, this would be computed from the Wealth module, but overrides are useful for what-if simulations)
    manual_annual_income = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Override system calculated income")
    manual_annual_expenses = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Override system calculated expenses")
    manual_current_net_worth = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    manual_investment_portfolio = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    
    # Lifestyle Scenarios
    FIRE_SCENARIOS = [
        ('lean', 'Lean FIRE (Minimal Lifestyle)'),
        ('regular', 'Regular FIRE (Current Lifestyle)'),
        ('fat', 'Fat FIRE (Luxury Lifestyle)'),
        ('coast', 'Coast FIRE (No more contributions needed)'),
        ('barista', 'Barista FIRE (Part-time work in retirement)'),
    ]
    selected_scenario = models.CharField(max_length=20, choices=FIRE_SCENARIOS, default='regular')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"FIRE Profile for {self.user.username}"


class FIRESimulationCache(models.Model):
    """
    Caches the results of the complex FIRE Monte Carlo / Deterministic simulation engine.
    This prevents heavy recalculation on every dashboard load.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='fire_simulation')
    
    calculated_fire_number = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    years_to_fire = models.DecimalField(max_digits=5, decimal_places=1, default=Decimal('0.0'))
    projected_fire_date = models.DateField(null=True, blank=True)
    current_savings_rate = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    
    # Timeline data for the charts (e.g., JSON array of {year, age, projected_wealth, fire_target})
    timeline_data = models.TextField(blank=True, default="[]", help_text="JSON serialized timeline progression")
    
    last_calculated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Simulation Cache for {self.user.username}"
