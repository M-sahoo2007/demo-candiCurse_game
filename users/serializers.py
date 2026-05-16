from rest_framework import serializers
from .models import UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = UserProfile.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user

class ProfileSerializer(serializers.ModelSerializer):
    best_score = serializers.IntegerField(read_only=True)
    games_played = serializers.IntegerField(read_only=True)
    leaderboard_rank = serializers.IntegerField(read_only=True)

    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'avatar', 'total_score', 'highest_level', 'best_score', 'games_played', 'leaderboard_rank', 'date_joined']
