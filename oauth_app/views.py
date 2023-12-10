###############################################################################
# From https://www.youtube.com/watch?v=yO6PP0vEOMc
# Author: Akamai DevRel
# Used: Rendering home page; however, the code was adapted to check
# authorization and if the user has an active game
###############################################################################
# From https://www.youtube.com/watch?v=yO6PP0vEOMc
# Author: Akamai DevRel
# Used: Creating the logout view
###############################################################################

from django.shortcuts import render, redirect
from django.contrib.auth import logout
from game_app.models import *

# Create your views here.

# From https://www.youtube.com/watch?v=yO6PP0vEOMc
def home(request):
    if request.user.is_authenticated:
        # Check if the user has a game currently, should only ever have 1 or 0
        has_game = ActiveGame.objects.filter(user=request.user).exists()
        return render(request, "home.html", {"has_game": has_game})
    return render(request, "login.html")


# From https://www.youtube.com/watch?v=yO6PP0vEOMc
def logout_view(request):
    logout(request)
    return redirect("/")


def login_game(request):
    return render(request, "login.html")
