from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='gamescore',
            index=models.Index(fields=['user'], name='gamescore_user_idx'),
        ),
        migrations.AddIndex(
            model_name='gamescore',
            index=models.Index(fields=['score'], name='gamescore_score_idx'),
        ),
    ]
