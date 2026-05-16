from django.urls import path
from .views import register_api, login_api, profile_api, save_score_api, leaderboard_api, game_history_api

urlpatterns = [
    path('register/', register_api, name='api_register'),
    path('login/', login_api, name='api_login'),
    path('profile/', profile_api, name='api_profile'),
    path('save-score/', save_score_api, name='api_save_score'),
    path('leaderboard/', leaderboard_api, name='api_leaderboard'),
    path('game-history/', game_history_api, name='api_game_history'),
]
