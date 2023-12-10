from django.shortcuts import render
from .models import UserStats  # Assuming your model is named UserStats


def leaderboard(request):
    sort_by = request.GET.get('sort', 'score')  # Default sort is by score

    if sort_by == 'games_played':
        top_users = UserStats.objects.all().order_by('-games_played')
    elif sort_by == 'locations_approved':
        top_users = UserStats.objects.all().order_by('-locations_approved')
    else:
        # Default sorting
        top_users = UserStats.objects.all().order_by('-score')

    return render(request, 'stats_app/leaderboard.html', {'top_users': top_users})
