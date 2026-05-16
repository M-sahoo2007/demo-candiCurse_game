from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    total_score = models.PositiveIntegerField(default=0)
    highest_level = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(default=timezone.now)

    @property
    def best_score(self):
        if hasattr(self, 'leaderboard_record') and self.leaderboard_record:
            return self.leaderboard_record.highest_score
        return 0

    @property
    def games_played(self):
        return self.scores.count()

    @property
    def leaderboard_rank(self):
        if hasattr(self, 'leaderboard_record') and self.leaderboard_record:
            return self.leaderboard_record.rank
        return 0

    def __str__(self):
        return self.username
