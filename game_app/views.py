###############################################################################
# Adapted from: Django practice
# Used: General structure for how to display objects in a view
###############################################################################
# Adapted from: Django practice
# Used: Creating a view that performs some action for an object instance
###############################################################################
# From: ChatGPT
# Used: How to set up a function that handles AJAX requests
###############################################################################
# From: https://stackoverflow.com/questions/22816704/django-get-a-random-object
# Author: lukeaus
# Used: Getting a random instance of an object
###############################################################################

from django.urls import reverse
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from .forms import GameForm
from stats.models import *
from .models import Game, ActiveGame
from django.views.generic import UpdateView, TemplateView, DetailView, ListView
from game_app.play import *
from django.http import JsonResponse
import random

# Radius within which the initial start location can be assigned
START_RADIUS = 0.005716


def add_game(request):
    if request.method == 'POST':
        form = GameForm(request.POST)
        if form.is_valid():
            form.save()
            # return redirect('add_location')
            return redirect('home')
    else:
        form = GameForm()

    context = {
        'form': form,
        'default_lat': 38.053,  # UVA
        'default_lng': -78.5035,
        'default_starting_hint': ""
    }

    return render(request, 'add_game.html', {'form': form})


# Adapted from: Django practice
class ApproveView(ListView):
    template_name = "approval.html"
    context_object_name = "game_submissions"

    def get_queryset(self):
        """
        Return the games that have been submitted for approval.
        """
        return Game.objects.filter(is_approved=False)[:1]

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_admin:
            return HttpResponseForbidden("Must be logged in with admin permissions.")

        return super().dispatch(request, *args, **kwargs)


# Adapted from: Django practice
def approve_game(request, pk):
    # Check if the user is an admin before performing approval
    if request.user.is_authenticated and request.user.is_admin:
        game = Game.objects.get(pk=pk)
        game.is_approved = True
        game.save()
        request.user.stats.locations_approved += 1
        request.user.stats.save()
    return redirect('approval')


# Adapted from: Django practice
def deny_game(request, pk):
    # Check if the user is an admin before performing denial
    if request.user.is_authenticated and request.user.is_admin:
        game = Game.objects.get(pk=pk)
        game.delete()

    return redirect('approval')


def static_play(request):
    # Must be logged in to play the game
    if not request.user.is_authenticated:
        return redirect('login_game')

    try:
        active_game = ActiveGame.objects.get(user=request.user)

        context0 = {
            'hint': active_game.get_curr_hint_display(),
            'lat': active_game.last_latitude,
            'lon': active_game.last_longitude,
            'is_tut': False,
            'starting_hint': active_game.game.starting_hint,
        }
        context1 = {
            'name': active_game.game.name,
            'hint_count': active_game.hint_counter,
        }
        context2 = {
            'hint': active_game.get_curr_hint_display(),
            'starting_hint': active_game.game.starting_hint,
            'lat': active_game.last_latitude,
            'lon': active_game.last_longitude,
            'dlat': active_game.game.latitude,
            'dlon': active_game.game.longitude,
            'is_tut': True,
        }
        if active_game.is_finished:
            return render(request, 'completed_game.html', context1)
        if active_game.is_tutorial:
            return render(request, 'static_play.html', context2)
        return render(request, 'static_play.html', context0)
    except ActiveGame.DoesNotExist:
        return HttpResponseForbidden("No game associated with this user.")


# From: ChatGPT
# Used: How to set up a function that handles AJAX requests
def update_hint(request):
    if request.method == 'GET':

        # This part was adapted from ChatGPT
        # Saw how to access request content but
        # changed it to grab the lat and lon instead
        latitude = request.GET.get('lat', None)
        longitude = request.GET.get('lng', None)

        if get_hint(request, latitude, longitude):
            # This part was from ChatGPT
            # Specifically: how to send JSON response
            return JsonResponse({'message': 'Coordinates received successfully'})

    return JsonResponse({'message': 'Invalid request'})


# View for getting the tutorial
def tutorial(request):
    if not request.user.is_authenticated:
        return redirect('login_game')

    try:
        # Remove any of the user's previous active games
        active_game = ActiveGame.objects.get(user=request.user)
        active_game.delete()
    except ActiveGame.DoesNotExist:
        do_nothing = 0
        # Do nothing if the user has no active games

    user = request.user
    game = None  # Should be set to the tutorial game
    try:
        # From: https://stackoverflow.com/questions/22816704/django-get-a-random-object
        # Author: lukeaus
        # Used: Getting a random instance
        all_games = list(Game.objects.filter(is_approved=True))
        game = random.choice(all_games)
    except Game.DoesNotExist:
        # No games available to play
        redirect('home')

    # Create the user's new active game
    ActiveGame.objects.create(user=user, game=game, hint_counter=0,
                              last_latitude=38.032243, last_longitude=-78.514473,
                              is_finished=False, is_tutorial=True, curr_hint=ActiveGame.Hint.NONE)

    return redirect('static_play')


# View for getting an easy game
def get_easy(request):
    if not request.user.is_authenticated:
        return redirect('login_game')

    try:
        # Remove any of the user's previous active games
        active_game = ActiveGame.objects.get(user=request.user)
        active_game.delete()
    except ActiveGame.DoesNotExist:
        do_nothing = 0
        # Do nothing if the user has no active games

    user = request.user
    rand_game = None  # Should be set to easy game
    try:
        # From: https://stackoverflow.com/questions/22816704/django-get-a-random-object
        # Author: lukeaus
        # Used: Getting a random instance
        all_games = list(Game.objects.filter(is_approved=True))
        rand_game = random.choice(all_games)
    except Game.DoesNotExist:
        # No games available to play
        redirect('home')

    # Initialize a random start location, centered on the tennis courts
    init_lat = float(rand_game.latitude) + START_RADIUS * random.uniform(-1, 1)
    init_lon = float(rand_game.longitude) + START_RADIUS * random.uniform(-1, 1)

    # Create the user's new active game
    ActiveGame.objects.create(user=user, game=rand_game, hint_counter=0,
                              last_latitude=init_lat, last_longitude=init_lon,
                              is_finished=False, curr_hint=ActiveGame.Hint.NONE)

    return redirect('static_play')


# View for getting a hard game
def get_hard(request):
    if not request.user.is_authenticated:
        return redirect('login_game')

    try:
        # Remove any of the user's previous active games
        active_game = ActiveGame.objects.get(user=request.user)
        active_game.delete()
    except ActiveGame.DoesNotExist:
        do_nothing = 0
        # Do nothing if the user has no active games

    user = request.user
    rand_game = None  # Should be set to easy game
    try:
        # From: https://stackoverflow.com/questions/22816704/django-get-a-random-object
        # Author: lukeaus
        # Used: Getting a random instance
        all_games = list(Game.objects.filter(is_approved=True))
        rand_game = random.choice(all_games)
    except Game.DoesNotExist:
        # No games available to play
        redirect('home')

    # Initialize a random start location, centered on the tennis courts
    init_lat = float(rand_game.latitude) + START_RADIUS * 1.5 + START_RADIUS * 2 * random.uniform(-1, 1)
    init_lon = float(rand_game.longitude) + START_RADIUS * 1.5 + START_RADIUS * 2 * random.uniform(-1, 1)

    # Create the user's new active game
    ActiveGame.objects.create(user=user, game=rand_game, hint_counter=0,
                              last_latitude=init_lat, last_longitude=init_lon,
                              is_finished=False, curr_hint=ActiveGame.Hint.NONE)

    return redirect('static_play')
