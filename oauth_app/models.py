###############################################################################
# From: ChatGPT
# Used: Extend AbstractUser to make a new model, fields were not from ChatGPT
###############################################################################

from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class AppUser(AbstractUser):
    # Toggle admin privileges
    is_admin = models.BooleanField(default=False)

    # User statistics
    games_played = models.IntegerField(default=0)

