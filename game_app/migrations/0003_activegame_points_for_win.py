# Generated by Django 4.2.4 on 2023-11-12 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_app', '0002_activegame'),
    ]

    operations = [
        migrations.AddField(
            model_name='activegame',
            name='points_for_win',
            field=models.IntegerField(default=100),
        ),
    ]