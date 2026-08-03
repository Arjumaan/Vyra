from django.db import models
from django.utils import timezone

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, help_text="e.g., USD, INR, EUR")
    name = models.CharField(max_length=50, help_text="e.g., US Dollar")
    symbol = models.CharField(max_length=10, help_text="e.g., $, ₹, €")
    is_base = models.BooleanField(default=False, help_text="Set to True for your primary currency")

    class Meta:
        verbose_name_plural = "Currencies"

    def __str__(self):
        return f"{self.code} - {self.name}"

    def save(self, *args, **kwargs):
        # Ensure only one base currency exists
        if self.is_base:
            Currency.objects.filter(is_base=True).update(is_base=False)
        super().save(*args, **kwargs)

class ExchangeRate(models.Model):
    from_currency = models.ForeignKey(Currency, related_name='exchange_rates_from', on_delete=models.CASCADE)
    to_currency = models.ForeignKey(Currency, related_name='exchange_rates_to', on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=18, decimal_places=6, help_text="Multiplier to convert from_currency to to_currency")
    date = models.DateField(default=timezone.now)
    is_manual = models.BooleanField(default=False, help_text="True if rate was manually overridden")

    class Meta:
        unique_together = ('from_currency', 'to_currency', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"1 {self.from_currency.code} = {self.rate} {self.to_currency.code} on {self.date}"
