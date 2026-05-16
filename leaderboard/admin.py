from django.contrib import admin
from .models import Leaderboard

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user', 'highest_score', 'rank', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username',)
