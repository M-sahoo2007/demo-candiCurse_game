from django.contrib import admin
from .models import GameScore

@admin.register(GameScore)
class GameScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'level', 'moves_used', 'mode', 'created_at')
    list_filter = ('mode', 'level', 'created_at')
    search_fields = ('user__username',)
