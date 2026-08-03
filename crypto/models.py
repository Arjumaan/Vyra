from django.db import models
from django.contrib.auth.models import User
import datetime

class CryptoHolding(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin_name = models.CharField(max_length=100)
    coin_symbol = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=20, decimal_places=8)
    buy_price = models.DecimalField(max_digits=14, decimal_places=2)
    current_price = models.DecimalField(max_digits=14, decimal_places=2)
    purchase_date = models.DateField(default=datetime.date.today)
    
    # New analytics fields
    category = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., Layer 1, DeFi, Meme")
    risk_level = models.CharField(max_length=20, choices=[('Medium', 'Medium'), ('High', 'High'), ('Extreme', 'Extreme')], default='High')
    
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.coin_symbol} - {self.coin_name}"

    def invested_amount(self):
        return float(self.quantity) * float(self.buy_price)

    def current_value(self):
        return float(self.quantity) * float(self.current_price)

    def profit_loss(self):
        return self.current_value() - self.invested_amount()

    def return_percent(self):
        if self.invested_amount() > 0:
            return round((self.profit_loss() / self.invested_amount()) * 100, 2)
        return 0
