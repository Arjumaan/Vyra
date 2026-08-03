from django.db import models
from django.contrib.auth.models import User

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    date = models.DateField()
    mood_score = models.IntegerField(default=5, help_text="1 to 10 scale")
    notes = models.TextField(blank=True, null=True, help_text="Daily financial reflections or thoughts")
    tags = models.CharField(max_length=200, blank=True, null=True, help_text="Comma separated tags")
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        unique_together = ('user', 'date')

    def __str__(self):
        return f"Journal on {self.date} by {self.user.username}"

class WishlistItem(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    STATUS_CHOICES = [
        ('planning', 'Planning to Buy'),
        ('saving', 'Saving For'),
        ('bought', 'Bought'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    item_name = models.CharField(max_length=200)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planning')
    
    target_date = models.DateField(blank=True, null=True)
    product_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.item_name} ({self.status})"
