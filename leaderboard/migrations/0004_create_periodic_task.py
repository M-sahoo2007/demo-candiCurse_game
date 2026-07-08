from django.db import migrations


def create_periodic_task(apps, schema_editor):
    try:
        IntervalSchedule = apps.get_model('django_celery_beat', 'IntervalSchedule')
        PeriodicTask = apps.get_model('django_celery_beat', 'PeriodicTask')
        # create or get 5-minute schedule
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=5,
            period=IntervalSchedule.MINUTES,
        )
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Recalculate leaderboard ranks (every 5 minutes)',
            task='leaderboard.tasks.recalculate_ranks',
        )
    except Exception:
        # django-celery-beat not installed or migrations not applied; skip gracefully
        pass


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0003_add_indexes'),
    ]

    operations = [
        migrations.RunPython(create_periodic_task, migrations.RunPython.noop),
    ]
