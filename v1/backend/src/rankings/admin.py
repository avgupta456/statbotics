from django.contrib import admin

from .models import Event, Match, Team, TeamEvent, TeamMatch, TeamYear, Year


class YearAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "elo_acc",
        "elo_mse",
        "opr_acc",
        "opr_mse",
        "mix_acc",
        "mix_mse",
        "rp1_acc",
        "rp1_mse",
        "rp2_acc",
        "rp2_mse",
        "score_sd",
        "score_mean",
    )


class TeamAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "name",
        "state",
        "country",
        "district",
        "active",
        "elo",
        "elo_recent",
        "elo_mean",
        "elo_max",
        "wins",
        "losses",
        "ties",
        "count",
        "winrate",
    )


class TeamYearAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "team",
        "name",
        "state",
        "country",
        "district",
        "elo_start",
        "elo_pre_champs",
        "elo_end",
        "elo_mean",
        "elo_max",
        "elo_diff",
        "opr",
        "opr_auto",
        "opr_teleop",
        "opr_1",
        "opr_2",
        "opr_endgame",
        "ils_1",
        "ils_2",
        "wins",
        "losses",
        "ties",
        "count",
        "elo_rank",
        "elo_percentile",
        "opr_rank",
        "opr_percentile",
    )


class EventAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "year",
        "name",
        "time",
        "state",
        "country",
        "district",
        "type",
        "week",
        "status",
        "elo_top8",
        "elo_top24",
        "elo_mean",
        "opr_top8",
        "opr_top24",
        "opr_mean",
        "elo_acc",
        "elo_mse",
        "opr_acc",
        "opr_mse",
        "mix_acc",
        "mix_mse",
        "rp1_acc",
        "rp1_mse",
        "rp2_acc",
        "rp2_mse",
    )


class TeamEventAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "year",
        "event",
        "time",
        "team_name",
        "event_name",
        "state",
        "country",
        "district",
        "type",
        "week",
        "status",
        "elo_start",
        "elo_pre_playoffs",
        "elo_end",
        "elo_mean",
        "elo_max",
        "elo_diff",
        "opr_start",
        "opr_end",
        "opr_auto",
        "opr_teleop",
        "opr_1",
        "opr_2",
        "opr_endgame",
        "ils_1_start",
        "ils_2_start",
        "ils_1_end",
        "ils_2_end",
        "wins",
        "losses",
        "ties",
        "count",
        "winrate",
        "rank",
    )


class MatchAdmin(admin.ModelAdmin):
    list_display = (
        "key",
        "year",
        "event",
        "comp_level",
        "set_number",
        "match_number",
        "playoff",
        "time",
        "status",
        "red",
        "blue",
        "red_score",
        "blue_score",
        "winner",
        "elo_winner",
        "elo_win_prob",
        "opr_winner",
        "opr_win_prob",
        "mix_winner",
        "mix_win_prob",
        "red_rp_1",
        "red_rp_1_prob",
        "red_rp_2",
        "red_rp_2_prob",
        "blue_rp_1",
        "blue_rp_1_prob",
        "blue_rp_2",
        "blue_rp_2_prob",
    )


class TeamMatchAdmin(admin.ModelAdmin):
    list_display = (
        "team",
        "year",
        "event",
        "match",
        "playoff",
        "alliance",
        "time",
        "status",
        "elo",
        "opr",
        "ils_1",
        "ils_2",
    )


admin.site.register(Year, YearAdmin)  # type: ignore
admin.site.register(Team, TeamAdmin)  # type: ignore
admin.site.register(TeamYear, TeamYearAdmin)  # type: ignore
admin.site.register(Event, EventAdmin)  # type: ignore
admin.site.register(TeamEvent, TeamEventAdmin)  # type: ignore
admin.site.register(Match, MatchAdmin)  # type: ignore
admin.site.register(TeamMatch, TeamMatchAdmin)  # type: ignore
