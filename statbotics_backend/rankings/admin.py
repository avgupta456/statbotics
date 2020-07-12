from django.contrib import admin

from .models import Year, Team, TeamYear, Event, TeamEvent, Match, TeamMatch


class YearAdmin(admin.ModelAdmin):
    list_display = ('year', 'elo_acc', 'elo_mse', 'opr_acc', 'opr_mse',
                    'mix_acc', 'mix_mse', 'rp1_acc', 'rp1_mse', 'rp2_acc',
                    'rp2_mse')


class TeamAdmin(admin.ModelAdmin):
    list_display = ('team', 'name', 'state', 'country', 'district',
                    'active', 'elo', 'elo_recent', 'elo_mean', 'elo_max')


class TeamYearAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'team', 'name', 'state', 'country',
                    'district', 'elo_start', 'elo_pre_champs', 'elo_end',
                    'elo_mean', 'elo_max', 'elo_diff', 'opr', 'opr_auto',
                    'opr_teleop', 'opr_1', 'opr_2', 'opr_endgame', 'ils_1',
                    'ils_2')


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'key', 'name', 'state', 'country',
                    'district', 'type', 'week', 'elo_top8', 'elo_top24',
                    'elo_mean', 'opr_top8', 'opr_top24', 'opr_mean')


class TeamEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'year', 'event', 'elo_start',
                    'elo_pre_playoffs', 'elo_end', 'elo_mean', 'elo_max',
                    'elo_diff', 'opr_start', 'opr_end', 'opr_auto',
                    'opr_teleop', 'opr_1', 'opr_2', 'opr_endgame',
                    'ils_1_start', 'ils_2_start', 'ils_1_end', 'ils_2_end')


class MatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'event', 'key', 'comp_level', 'set_number',
                    'match_number', 'playoff', 'winner', 'elo_winner',
                    'elo_win_prob', 'opr_winner', 'opr_win_prob', 'mix_winner',
                    'mix_win_prob', 'red_rp_1', 'red_rp_1_prob', 'red_rp_2',
                    'red_rp_2_prob', 'blue_rp_1', 'blue_rp_1_prob',
                    'blue_rp_2', 'blue_rp_2_prob')


class TeamMatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'team', 'year', 'event', 'match', 'alliance',
                    'elo', 'opr', 'ils_1', 'ils_2')


admin.site.register(Year, YearAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(TeamYear, TeamYearAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(TeamEvent, TeamEventAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(TeamMatch, TeamMatchAdmin)
