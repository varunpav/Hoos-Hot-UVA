###############################################################################
# From https://www.youtube.com/watch?v=yO6PP0vEOMc
# Author: Akamai DevRel
# Used: Initial setup of routing
###############################################################################

from django.urls import path, include
from . import views



urlpatterns = [

    #From https://www.youtube.com/watch?v=yO6PP0vEOMc
    path("", views.home, name='home'),
    path("logout", views.logout_view),
    path('game/', include('game_app.urls')),
    path('login_game', views.login_game, name ='login_game')

]
