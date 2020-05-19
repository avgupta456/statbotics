from django.contrib import admin
from .models import TeamMatch, TeamEvent, TeamYear, Team, Event, Year

class TeamMatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'event', 'match',
        'team', 'elo_start', 'elo_end', 'elo_diff')

class TeamEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'event', 'team', 'elo_start',
        'elo_pre_playoffs', 'elo_end', 'elo_mean', 'elo_max', 'elo_diff')

class TeamYearAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'team', 'elo_start', 'elo_pre_champs',
        'elo_end', 'elo_mean', 'elo_max', 'elo_diff', 'rank', 'percentile')

class TeamAdmin(admin.ModelAdmin):
    list_display = ('team', 'elo', 'elos', 'elo_mean', 'elo_max', 'elo_max_year')

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'event', 'elo_max', 'elo_top8', 'elo_top24', 'elo_mean', 'elo_sd')

class YearAdmin(admin.ModelAdmin):
    list_display = ('year', 'elo_max', 'elo_1p', 'elo_5p', 'elo_10p', 'elo_25p',
        'elo_median', 'elo_mean', 'elo_sd', 'acc', 'mse')

admin.site.register(TeamMatch, TeamMatchAdmin)
admin.site.register(TeamEvent, TeamEventAdmin)
admin.site.register(TeamYear, TeamYearAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Year, YearAdmin)
