from celery import shared_task
from django.db import transaction
from .models import Leaderboard


@shared_task
def recalculate_ranks(batch_size=1000):
    """Recalculate ranks for all leaderboard entries in bulk.
    This function orders Leaderboard by highest_score desc and assigns incremental ranks.
    It updates in batches to avoid large transactions.
    """
    qs = Leaderboard.objects.order_by('-highest_score', 'user_id').values_list('pk', flat=True)
    pks = list(qs)
    total = len(pks)
    if total == 0:
        return {'updated': 0}

    updated = 0
    # process in batches
    for start in range(0, total, batch_size):
        end = start + batch_size
        batch_pks = pks[start:end]
        batch_objs = list(Leaderboard.objects.filter(pk__in=batch_pks).order_by('-highest_score', 'user_id'))
        to_update = []
        for offset, obj in enumerate(batch_objs, start=start + 1):
            if obj.rank != offset:
                obj.rank = offset
                to_update.append(obj)
        if to_update:
            Leaderboard.objects.bulk_update(to_update, ['rank'])
            updated += len(to_update)
    return {'updated': updated}
