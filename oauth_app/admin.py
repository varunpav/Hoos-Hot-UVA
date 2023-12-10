###############################################################################
# From: ChatGPT (Edited example given to fit project, not exact copy paste)
# Used: Setting up a new admin dashboard / page
###############################################################################

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from oauth_app.models import AppUser


# New admin dashboard so user info can be edited from admin panel
# From: ChatGPT (Edited example given to fit project)
class AppUserAdmin(UserAdmin):
    search_fields = ('username', 'email')
    ordering = ('username',)
    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        ('Custom Fields', {'fields': ('is_admin',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('is_admin',),
        }),
    )


# Register your models here.
admin.site.register(AppUser, AppUserAdmin)
