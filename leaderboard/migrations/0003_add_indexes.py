from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaderboard', '0002_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='leaderboard',
            index=models.Index(fields=['highest_score'], name='leaderboard_highest_score_idx'),
        ),
    ]
