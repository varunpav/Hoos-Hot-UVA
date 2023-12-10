###############################################################################
# From: https://docs.djangoproject.com/en/4.2/ref/models/fields/
# Used: How to set up an enum field
###############################################################################


from django.db import models
from oauth_app.models import AppUser
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Game(models.Model):
    # Game name
    name = models.CharField(max_length=128)

    # Newly created Games should be approved by admins before they becom available
    is_approved = models.BooleanField(default=False)

    # Using 6 decimal places should be accurate enough
    # Google Maps API only gives 6
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    starting_hint = models.CharField(max_length=128, default="")

    def __str__(self):
        return f"({self.name}, approved: {self.is_approved}, {self.latitude}, {self.longitude},{self.starting_hint})"


class ActiveGame(models.Model):
    # From: https://docs.djangoproject.com/en/4.2/ref/models/fields/
    class Hint(models.TextChoices):
        HOT = "H", _("HOT")
        COLD = "C", _("COLD")
        WARM = "W", _("WARM")
        COOLER = "CR", _("COOLER")
        NONE = "N", _("REQUEST HINT")



    # The user playing the game
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)

    # The game being played
    game = models.ForeignKey(Game, on_delete=models.CASCADE)


    # Track number of hints requested and what is the current hint
    curr_hint = models.CharField(
        max_length=2,
        choices=Hint.choices,
        default=Hint.NONE
    )
    hint_counter = models.IntegerField(default=0)

    # Fields to track coordinates of last guess
    last_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    last_longitude = models.DecimalField(max_digits=9, decimal_places=6)

    # Has this game been completed
    is_finished = models.BooleanField(default=False)

    # Used for special active games played as tutorials
    is_tutorial = models.BooleanField(default=False)

    # Used for score calculation
    points_for_win = models.IntegerField(default=100)
