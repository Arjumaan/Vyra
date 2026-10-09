from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Property(models.Model):
    PROPERTY_TYPES = [
        ('RESIDENTIAL', 'Residential'),
        ('COMMERCIAL', 'Commercial'),
        ('LAND', 'Land'),
        ('VACATION', 'Vacation Home'),
        ('OTHER', 'Other'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='real_estate_properties')
    name = models.CharField(max_length=200, help_text="e.g. Downtown Condo")
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, default='RESIDENTIAL')
    address = models.TextField(blank=True, null=True)
    
    # Valuations
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    down_payment = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Yield / Cash Flow
    monthly_rental_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monthly_operating_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Mortgage / Debt
    has_mortgage = models.BooleanField(default=False)
    mortgage_balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    mortgage_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    mortgage_monthly_payment = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.get_property_type_display()})"

    @property
    def equity(self):
        return self.current_value - self.mortgage_balance
        
    @property
    def annual_gross_rent(self):
        return self.monthly_rental_income * Decimal('12')
        
    @property
    def annual_net_operating_income(self):
        return (self.monthly_rental_income - self.monthly_operating_expenses) * Decimal('12')
        
    @property
    def cap_rate(self):
        if self.current_value <= 0: return Decimal('0')
        return (self.annual_net_operating_income / self.current_value) * Decimal('100')
        
    @property
    def annual_cash_flow(self):
        return self.annual_net_operating_income - (self.mortgage_monthly_payment * Decimal('12'))
        
    @property
    def cash_on_cash_return(self):
        if self.down_payment <= 0: return Decimal('0')
        return (self.annual_cash_flow / self.down_payment) * Decimal('100')

    @property
    def gross_yield(self):
        if self.current_value <= 0: return Decimal('0')
        return (self.annual_gross_rent / self.current_value) * Decimal('100')
