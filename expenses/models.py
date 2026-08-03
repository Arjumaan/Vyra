from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"
        unique_together = ('user', 'category_name')

    def __str__(self):
        return self.category_name

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    
    # OCR & Receipt Tracking
    receipt_image = models.ImageField(upload_to='receipts/', blank=True, null=True)
    ocr_processed = models.BooleanField(default=False, help_text="Has this receipt been processed by the OCR engine?")
    ocr_text = models.TextField(blank=True, null=True, help_text="Raw text extracted from OCR")

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.user.username} - {self.category} - {self.amount}"
