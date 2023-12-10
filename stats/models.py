from django.conf import settings
from django.db import models


class UserStats(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stats')
    score = models.PositiveIntegerField(default=0)
    locations_approved = models.PositiveIntegerField(default=0)
    games_played = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.user.username
