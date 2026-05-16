from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import RegisterSerializer, ProfileSerializer
from game.models import GameScore
from leaderboard.models import Leaderboard
from .serializers import ScoreSerializer, LeaderboardSerializer, GameHistorySerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        Leaderboard.objects.get_or_create(user=user, defaults={'highest_score': 0, 'rank': 0})
        return Response({'message': 'Registered successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        tokens = get_tokens_for_user(user)
        profile = ProfileSerializer(user)
        return Response({'tokens': tokens, 'profile': profile.data})
    return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def profile_api(request):
    serializer = ProfileSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_score_api(request):
    serializer = ScoreSerializer(data=request.data)
    if serializer.is_valid():
        GameScore.objects.create(
            user=request.user,
            score=serializer.validated_data['score'],
            level=serializer.validated_data['level'],
            moves_used=serializer.validated_data.get('moves_used', 0),
            mode=serializer.validated_data.get('mode', 'moves'),
        )
        request.user.total_score += serializer.validated_data['score']
        request.user.highest_level = max(request.user.highest_level, serializer.validated_data['level'])
        request.user.save()
        leaderboard, _ = Leaderboard.objects.get_or_create(user=request.user)
        leaderboard.highest_score = max(leaderboard.highest_score, serializer.validated_data['score'])
        leaderboard.save()
        rank = Leaderboard.objects.filter(highest_score__gt=leaderboard.highest_score).count() + 1
        leaderboard.rank = rank
        leaderboard.save(update_fields=['rank'])
        return Response({
            'message': 'Score saved successfully.',
            'total_score': request.user.total_score,
            'best_score': leaderboard.highest_score,
            'rank': rank,
        })
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def leaderboard_api(request):
    leaders = Leaderboard.objects.order_by('-highest_score')[:20]
    serializer = LeaderboardSerializer(leaders, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def game_history_api(request):
    history = GameScore.objects.filter(user=request.user).order_by('-created_at')[:20]
    serializer = GameHistorySerializer(history, many=True)
    return Response(serializer.data)
