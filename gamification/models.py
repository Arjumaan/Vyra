from django.db import models
from django.contrib.auth.models import User

class VyraScore(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='vyra_score')
    score = models.IntegerField(default=0, help_text="Total gamification points")
    level = models.IntegerField(default=1)
    current_streak_days = models.IntegerField(default=0, help_text="Consecutive days logging in/adding transactions")
    longest_streak_days = models.IntegerField(default=0)
    
    last_activity_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - Level {self.level} (Score: {self.score})"

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=100, help_text="CSS class or image path for the badge icon")
    points_awarded = models.IntegerField(default=10)

    def __str__(self):
        return self.name

class UserBadge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'badge')

    def __str__(self):
        return f"{self.user.username} earned {self.badge.name}"
