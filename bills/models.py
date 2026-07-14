from django.db import models
from django.contrib.auth.models import User
import datetime

class Bill(models.Model):
    BILL_CATEGORIES = [
        ('electricity', 'Electricity'), ('internet', 'Internet'),
        ('water', 'Water'), ('mobile', 'Mobile'), ('gas', 'Gas'),
        ('ott', 'OTT Subscription'), ('rent', 'Rent'),
        ('maintenance', 'Maintenance'), ('other', 'Other'),
    ]
    FREQUENCIES = [
        ('monthly', 'Monthly'), ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'), ('one_time', 'One Time'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bill_name = models.CharField(max_length=150)
    category = models.CharField(max_length=30, choices=BILL_CATEGORIES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    due_date = models.DateField()
    frequency = models.CharField(max_length=20, choices=FREQUENCIES, default='monthly')
    is_paid = models.BooleanField(default=False)
    auto_recurring = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bill_name} - ₹{self.amount}"

    def days_until_due(self):
        delta = self.due_date - datetime.date.today()
        return delta.days

    def is_overdue(self):
        return self.due_date < datetime.date.today() and not self.is_paid
