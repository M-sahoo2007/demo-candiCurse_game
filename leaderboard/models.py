from django.db import models
from django.conf import settings
from django.utils import timezone

class Leaderboard(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='leaderboard_record')
    highest_score = models.PositiveIntegerField(default=0)
    rank = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-highest_score']

    def __str__(self):
        return f'{self.user.username} - {self.highest_score}'
