from django.contrib.auth import authenticate
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import RegisterSerializer, ProfileSerializer
from game.models import GameScore
from leaderboard.models import Leaderboard
from .serializers import ScoreSerializer, LeaderboardSerializer, GameHistorySerializer
from django.db import transaction
from leaderboard.tasks import recalculate_ranks


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
        score_val = serializer.validated_data['score']
        level_val = serializer.validated_data['level']
        # Use a transaction and select_for_update to avoid race conditions and reduce writes.
        with transaction.atomic():
            GameScore.objects.create(
                user=request.user,
                score=score_val,
                level=level_val,
                moves_used=serializer.validated_data.get('moves_used', 0),
                mode=serializer.validated_data.get('mode', 'moves'),
            )
            # Update user aggregates in memory and save once if changed.
            user_updated_fields = []
            new_total = getattr(request.user, 'total_score', 0) + score_val
            if new_total != getattr(request.user, 'total_score', 0):
                request.user.total_score = new_total
                user_updated_fields.append('total_score')
            new_highest_level = max(getattr(request.user, 'highest_level', 0), level_val)
            if new_highest_level != getattr(request.user, 'highest_level', 0):
                request.user.highest_level = new_highest_level
                user_updated_fields.append('highest_level')
            if user_updated_fields:
                request.user.save(update_fields=user_updated_fields)

            leaderboard, _ = Leaderboard.objects.select_for_update().get_or_create(user=request.user, defaults={'highest_score': 0, 'rank': 0})
            old_high = leaderboard.highest_score
            new_high = max(old_high, score_val)
            if new_high != old_high:
                leaderboard.highest_score = new_high
                # compute rank (this is O(n); consider offloading to background job for large datasets)
                rank = Leaderboard.objects.filter(highest_score__gt=new_high).count() + 1
                leaderboard.rank = rank
                leaderboard.save(update_fields=['highest_score', 'rank'])
            else:
                rank = leaderboard.rank
            # enqueue background rank recalculation to keep ranks consistent
            try:
                recalculate_ranks.delay()
            except Exception:
                # avoid failing the request if Celery isn't available
                pass
        return Response({
            'message': 'Score saved successfully.',
            'total_score': getattr(request.user, 'total_score', 0),
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
