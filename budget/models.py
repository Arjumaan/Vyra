from django.db import models
from django.contrib.auth.models import User
import datetime

class Budget(models.Model):
    MONTH_CHOICES = [
        (1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'),
        (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'),
        (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    monthly_budget = models.DecimalField(max_digits=12, decimal_places=2)
    month = models.IntegerField(choices=MONTH_CHOICES, default=datetime.datetime.now().month)
    year = models.IntegerField(default=datetime.datetime.now().year)

    class Meta:
        unique_together = ('user', 'month', 'year')

    def __str__(self):
        return f"{self.user.username} - {self.get_month_display()} {self.year} - {self.monthly_budget}"
