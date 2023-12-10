from django.contrib import admin
from .models import UserStats

@admin.register(UserStats)
class UserStatsAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'games_played')
