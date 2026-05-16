from rest_framework import serializers
from users.serializers import ProfileSerializer, RegisterSerializer
from game.models import GameScore
from leaderboard.models import Leaderboard

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScore
        fields = ['id', 'user', 'score', 'level', 'moves_used', 'mode', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class LeaderboardSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()

    class Meta:
        model = Leaderboard
        fields = ['user', 'highest_score', 'rank', 'created_at']

class GameHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = GameScore
        fields = ['id', 'score', 'level', 'moves_used', 'mode', 'created_at']
