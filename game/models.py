from django.db import models
from django.conf import settings
from django.utils import timezone

class GameScore(models.Model):
    MODE_CHOICES = [
        ('moves', 'Limited Moves'),
        ('timer', 'Timer Mode'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='scores')
    score = models.PositiveIntegerField(default=0)
    level = models.PositiveIntegerField(default=1)
    moves_used = models.PositiveIntegerField(default=0)
    mode = models.CharField(max_length=16, choices=MODE_CHOICES, default='moves')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f'{self.user.username} - {self.score} pts'
