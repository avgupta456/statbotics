from django.contrib import admin
from .models import Team

class TeamAdmin(admin.ModelAdmin):
    list_display = ('number', 'name')

admin.site.register(Team, TeamAdmin)
