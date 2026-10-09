from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class BusinessProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='businesses')
    name = models.CharField(max_length=200, help_text="e.g. Freelance Consulting, Etsy Shop")
    business_type = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
        
    @property
    def total_revenue(self):
        return sum((t.amount for t in self.transactions.filter(transaction_type='INCOME')), Decimal('0'))
        
    @property
    def total_expenses(self):
        return sum((t.amount for t in self.transactions.filter(transaction_type='EXPENSE')), Decimal('0'))
        
    @property
    def net_profit(self):
        return self.total_revenue - self.total_expenses
        
    @property
    def profit_margin(self):
        if self.total_revenue <= Decimal('0'): return Decimal('0')
        return (self.net_profit / self.total_revenue) * Decimal('100')

class BusinessTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('INCOME', 'Income (Revenue)'),
        ('EXPENSE', 'Expense (Cost)'),
    ]
    business = models.ForeignKey(BusinessProfile, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=300)
    client_or_vendor = models.CharField(max_length=200, blank=True, null=True, help_text="Who paid you or who you paid")
    
    # Tax tracking
    is_tax_deductible = models.BooleanField(default=False, help_text="Can this expense be deducted?")
    tax_category = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. Software, Travel, Meals")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.business.name} - {self.get_transaction_type_display()} - {self.amount}"
