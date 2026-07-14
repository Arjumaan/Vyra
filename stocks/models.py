from django.db import models
from django.contrib.auth.models import User
import datetime

class Stock(models.Model):
    EXCHANGES = [('NSE', 'NSE'), ('BSE', 'BSE'), ('NYSE', 'NYSE'), ('NASDAQ', 'NASDAQ'), ('OTHER', 'Other')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=200)
    stock_symbol = models.CharField(max_length=20)
    exchange = models.CharField(max_length=10, choices=EXCHANGES, default='NSE')
    quantity = models.DecimalField(max_digits=12, decimal_places=4)
    buy_price = models.DecimalField(max_digits=12, decimal_places=2)
    current_price = models.DecimalField(max_digits=12, decimal_places=2)
    purchase_date = models.DateField(default=datetime.date.today)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.stock_symbol} - {self.company_name}"

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
