from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import render
from .models import Leaderboard
from game.models import GameScore


@login_required
def leaderboard_view(request):
    User = get_user_model()

    # Ensure every registered user has an associated leaderboard entry.
    for user in User.objects.all():
        Leaderboard.objects.get_or_create(user=user, defaults={'highest_score': 0, 'rank': 0})

    leaders = Leaderboard.objects.select_related('user').order_by('-highest_score', 'user__username')[:20]
    user_ids = [leader.user_id for leader in leaders]
    counts = {
        item['user']: item['score_count']
        for item in GameScore.objects.filter(user_id__in=user_ids).values('user').annotate(score_count=Count('id'))
    }

    leaderboard_rows = []
    for rank, record in enumerate(leaders, start=1):
        leaderboard_rows.append({
            'rank': rank,
            'username': record.user.username,
            'highest_score': record.highest_score,
            'total_score': getattr(record.user, 'total_score', 0),
            'highest_level': getattr(record.user, 'highest_level', 0),
            'games_played': counts.get(record.user_id, 0),
            'joined': record.user.date_joined,
            'is_self': record.user == request.user,
        })
        if record.rank != rank:
            record.rank = rank
            record.save(update_fields=['rank'])

    return render(request, 'leaderboard.html', {'leaders': leaderboard_rows})
