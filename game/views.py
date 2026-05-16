from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from leaderboard.models import Leaderboard


@login_required
def game_index(request):
    leaderboard, _ = Leaderboard.objects.get_or_create(
        user=request.user,
        defaults={'highest_score': 0, 'rank': 0}
    )
    return render(request, 'game.html', {
        'username': request.user.username,
        'total_score': request.user.total_score,
        'best_score': leaderboard.highest_score,
        'highest_level': request.user.highest_level,
        'leaderboard_rank': leaderboard.rank,
    })
