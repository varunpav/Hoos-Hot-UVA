###############################################################################
# URL: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
# Author: Kurt Peek
# Used: How to use GeoPy to find distance between two points
###############################################################################

from geopy.distance import geodesic
from oauth_app.models import *
from stats.models import *
from .models import *

# User must be within this many meters of the objective to discover it
DESTINATION_RADIUS = 20


# User points starting values
# May need to describe logic to users:
# Simple idea is 100 points and every hint subtracts 5 points until 0


# Returns distance in meters
def geo_distance(lat_0, lon_0, lat_1, lon_1):
    # URL: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    # Author: Kurt Peek
    # Used: How to use GeoPy to find distance between two points
    point_0 = (lat_0, lon_0)
    point_1 = (lat_1, lon_1)
    return geodesic(point_0, point_1).kilometers * 1000


def get_hint(request, guess_lat, guess_lon):
    try:
        active_game = ActiveGame.objects.get(user=request.user)
    except ActiveGame.DoesNotExist:
        return False
    game = active_game.game

    prev_dist = geo_distance(active_game.last_latitude, active_game.last_longitude, game.latitude, game.longitude)
    guess_dist = geo_distance(guess_lat, guess_lon, game.latitude, game.longitude)

    if guess_dist < prev_dist / 2:
        active_game.curr_hint = "H"
    elif guess_dist < prev_dist:
        active_game.curr_hint = "W"
    elif guess_dist > prev_dist * 1.5:
        active_game.curr_hint = "C"
    else:
        active_game.curr_hint = "CR"

    active_game.hint_counter += 1
    active_game.points_for_win -= 5
    active_game.last_latitude = guess_lat
    active_game.last_longitude = guess_lon

    if guess_dist < DESTINATION_RADIUS:
        active_game.is_finished = True
        if not active_game.is_tutorial:
            user_stats, created = UserStats.objects.get_or_create(user=active_game.user)
            user_stats.games_played += 1
            user_stats.score += active_game.points_for_win
            user_stats.save()

    active_game.save()
    return True
