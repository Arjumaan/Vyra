from django.db import models
from django.contrib.auth.models import User

class FamilyGroup(models.Model):
    name = models.CharField(max_length=100, help_text="e.g., The Smith Family")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Administrator'),
        ('Member', 'Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='family_member')
    group = models.ForeignKey(FamilyGroup, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='Member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'group')

    def __str__(self):
        return f"{self.user.username} - {self.group.name} ({self.role})"
