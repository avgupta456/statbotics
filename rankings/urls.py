from django.conf.urls import url
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import SwaggerUIRenderer, get_schema_view
from rest_framework import permissions, routers

from rankings.views import (
    event_pred_views,
    event_views,
    match_views,
    model_views,
    team_event_views,
    team_match_views,
    team_views,
    team_year_views,
    year_views,
)

SwaggerUIRenderer.template = "drf-yasg.html"  # monkey-patching is bad :(

schema_view = get_schema_view(
    openapi.Info(title="Statbotics.io API", default_version="v1",),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r"_years", model_views.YearView, "year")
router.register(r"_teams", model_views.TeamView, "team")
router.register(r"_team_years", model_views.TeamYearView, "team_year")
router.register(r"_events", model_views.EventView, "event")
router.register(r"_team_events", model_views.TeamEventView, "team_event")
router.register(r"_matches", model_views.MatchView, "match")
router.register(r"_team_matches", model_views.TeamMatchView, "team_match")

# commented out url patterns still need models
urlpatterns = [
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
]

"""TEAMS"""
urlpatterns.extend(
    [
        path("api/team/<num>", team_views.Team),
        path("api/teams", team_views.Teams),
        path("api/teams/", team_views.Teams),
        path("api/teams/by/<metric>", team_views.TeamsByMetric),
        path("api/teams/active", team_views.TeamsActive),
        path("api/teams/active/by/<metric>", team_views.TeamsActiveByMetric),
        path("api/teams/country/<country>", team_views._Teams),
        path("api/teams/country/<country>/by/<metric>", team_views._Teams),
        path("api/teams/country/<country>/active", team_views._TeamsActive),
        path("api/teams/country/<country>/active/by/<metric>", team_views._TeamsActive),
        path("api/teams/country/<country>/state/<state>", team_views._Teams),
        path(
            "api/teams/country/<country>/state/<state>/by/<metric>", team_views._Teams
        ),
        path(
            "api/teams/country/<country>/state/<state>/active", team_views._TeamsActive
        ),
        path(
            "api/teams/country/<country>/state/<state>/active/by/<metric>",
            team_views._TeamsActive,
        ),
        path("api/teams/district/<district>", team_views._Teams),
        path("api/teams/district/<district>/by/<metric>", team_views._Teams),
        path("api/teams/district/<district>/active", team_views._TeamsActive),
        path(
            "api/teams/district/<district>/active/by/<metric>", team_views._TeamsActive
        ),
    ]
)

"""TEAM EVENTS"""
urlpatterns.extend(
    [
        path("api/team_year/team/<num>/year/<year>", team_year_views.TeamYear),
        path("api/team_years/team/<num>", team_year_views.TeamYearsNum),
        path(
            "api/team_years/team/<num>/by/<metric>",
            team_year_views.TeamYearsNumByMetric,
        ),
        path("api/team_years/year/<year>", team_year_views.TeamYearsYear),
        path(
            "api/team_years/year/<year>/by/<metric>",
            team_year_views.TeamYearsYearByMetric,
        ),
        path(
            "api/team_years/year/<year>/country/<country>", team_year_views._TeamYears
        ),
        path(
            "api/team_years/year/<year>/country/<country>/by/<metric>",
            team_year_views._TeamYears,
        ),
        path(
            "api/team_years/year/<year>/country/<country>/state/<state>",
            team_year_views._TeamYears,
        ),
        path(
            "api/team_years/year/<year>/country/<country>/state/<state>/by/<metric>",
            team_year_views._TeamYears,
        ),
        path(
            "api/team_years/year/<year>/district/<district>", team_year_views._TeamYears
        ),
        path(
            "api/team_years/year/<year>/district/<district>/by/<metric>",
            team_year_views._TeamYears,
        ),
        path("api/team_years/", team_year_views.TeamYears),
        path("api/team_years/page/<page>", team_year_views._TeamYears),
        path("api/team_years/by/<metric>", team_year_views.TeamYearsByMetric),
        path("api/team_years/by/<metric>/page/<page>", team_year_views._TeamYears),
        path("api/team_years/country/<country>", team_year_views._TeamYears),
        path(
            "api/team_years/country/<country>/page/<page>", team_year_views._TeamYears
        ),
        path(
            "api/team_years/country/<country>/by/<metric>", team_year_views._TeamYears
        ),
        path(
            "api/team_years/country/<country>/by/<metric>/page/<page>",
            team_year_views._TeamYears,
        ),
        path(
            "api/team_years/country/<country>/state/<state>", team_year_views._TeamYears
        ),
        path(
            "api/team_years/country/<country>/state/<state>/by/<metric>",
            team_year_views._TeamYears,
        ),
        path("api/team_years/district/<district>", team_year_views._TeamYears),
        path(
            "api/team_years/district/<district>/by/<metric>", team_year_views._TeamYears
        ),
    ]
)

"""TEAM EVENTS"""
urlpatterns.extend(
    [
        path("api/team_event/team/<num>/event/<event>", team_event_views.TeamEvent),
        path("api/team_events/team/<num>", team_event_views.TeamEventsNum),
        path(
            "api/team_events/team/<num>/by/<metric>",
            team_event_views.TeamEventsNumByMetric,
        ),
        path("api/team_events/team/<num>/type/<type>", team_event_views._TeamEvents),
        path(
            "api/team_events/team/<num>/type/<type>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/team/<num>/week/<week>", team_event_views._TeamEvents),
        path(
            "api/team_events/team/<num>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/team/<num>/type/<type>/week/<week>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/team/<num>/type/<type>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/year/<year>", team_event_views.TeamEventsYear),
        path("api/team_events/year/<year>/page/<page>", team_event_views._TeamEvents),
        path(
            "api/team_events/year/<year>/by/<metric>",
            team_event_views.TeamEventsYearByMetric,
        ),
        path(
            "api/team_events/year/<year>/by/<metric>/page/<page>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/year/<year>/type/<type>", team_event_views._TeamEvents),
        path(
            "api/team_events/year/<year>/type/<type>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/year/<year>/week/<week>", team_event_views._TeamEvents),
        path(
            "api/team_events/year/<year>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/country/<country>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/country/<country>/page/<page>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/country/<country>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/country/<country>/by/<metric>/page/<page>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/country/<country>/state/<state>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/country/<country>/state/<state>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/district/<district>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/district/<district>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/year/<year>/type/<type>", team_event_views._TeamEvents),
        path(
            "api/team_events/year/<year>/type/<type>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/country/<country>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/country/<country>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/country/<country>/state/<state>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/country/<country>/state/<state>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/district/<district>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/district/<district>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/year/<year>/week/<week>", team_event_views._TeamEvents),
        path(
            "api/team_events/year/<year>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/week/<week>/country/<country>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/week/<week>/country/<country>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/week/<week>/country/<country>/state/<state>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/week/<week>/country/<country>/state/<state>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/week/<week>/district/<district>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/week/<week>/district/<district>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>/country/<country>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>/country/<country>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>/country/<country>/state/<state>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>/country/<country>/state/<state>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>/district/<district>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/year/<year>/type/<type>/week/<week>/district/<district>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/team/<num>/year/<year>", team_event_views.TeamEventsNumYear
        ),
        path(
            "api/team_events/team/<num>/year/<year>/by/<metric>",
            team_event_views.TeamEventsNumYearByMetric,
        ),
        path(
            "api/team_events/team/<num>/year/<year>/type/<type>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/team/<num>/year/<year>/type/<type>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/team/<num>/year/<year>/week/<week>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/team/<num>/year/<year>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/team/<num>/year/<year>/type/<type>/week/<week>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/team/<num>/year/<year>/type/<type>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/event/<event>", team_event_views.TeamEventsEvent),
        path(
            "api/team_events/event/<event>/by/<metric>",
            team_event_views.TeamEventsEventByMetric,
        ),
        path("api/team_events", team_event_views.TeamEvents),
        path("api/team_events/page/<page>", team_event_views._TeamEvents),
        path("api/team_events/country/<country>", team_event_views._TeamEvents),
        path(
            "api/team_events/country/<country>/page/<page>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/country/<country>/state/<state>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/country/<country>/state/<state>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/district/<district>", team_event_views._TeamEvents),
        path(
            "api/team_events/district/<district>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/type/<type>", team_event_views._TeamEvents),
        path("api/team_events/type/<type>/by/<metric>", team_event_views._TeamEvents),
        path(
            "api/team_events/type/<type>/country/<country>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/country/<country>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/country/<country>/state/<state>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/country/<country>/state/<state>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/district/<district>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/district/<district>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/week/<week>", team_event_views._TeamEvents),
        path("api/team_events/week/<week>/by/<metric>", team_event_views._TeamEvents),
        path(
            "api/team_events/week/<week>/country/<country>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/week/<week>/country/<country>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/week/<week>/country/<country>/state/<state>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/week/<week>/country/<country>/state/<state>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/week/<week>/district/<district>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/week/<week>/district/<district>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path("api/team_events/type/<type>/week/<week>", team_event_views._TeamEvents),
        path(
            "api/team_events/type/<type>/week/<week>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/week/<week>/country/<country>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/week/<week>/country/<country>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/week/<week>/country/<country>/state/<state>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/week/<week>/country/<country>/state/<state>/by/<metric>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/week/<week>/district/<district>",
            team_event_views._TeamEvents,
        ),
        path(
            "api/team_events/type/<type>/week/<week>/district/<district>/by/<metric>",
            team_event_views._TeamEvents,
        ),
    ]
)

"""TEAM MATCHES"""
urlpatterns.extend(
    [
        path("api/team_match/team/<num>/match/<match>", team_match_views.TeamMatch),
        path("api/team_matches", team_match_views.TeamMatches),
        path("api/team_matches/elims", team_match_views._TeamMatchesElim),
        path("api/team_matches/page/<page>", team_match_views._TeamMatches),
        path("api/team_matches/page/<page>/elims", team_match_views._TeamMatchesElim),
        path("api/team_matches/team/<num>", team_match_views.TeamMatchesTeam),
        path("api/team_matches/team/<num>/elims", team_match_views._TeamMatchesElim),
        path("api/team_matches/year/<year>", team_match_views.TeamMatchesYear),
        path("api/team_matches/year/<year>/elims", team_match_views._TeamMatchesElim),
        path("api/team_matches/year/<year>/page/<page>", team_match_views._TeamMatches),
        path(
            "api/team_matches/year/<year>/page/<page>",
            team_match_views._TeamMatchesElim,
        ),
        path("api/team_matches/event/<event>", team_match_views.TeamMatchesEvent),
        path("api/team_matches/event/<event>/elims", team_match_views._TeamMatchesElim),
        path("api/team_matches/match/<match>", team_match_views.TeamMatchesMatch),
        path(
            "api/team_matches/team/<num>/year/<year>",
            team_match_views.TeamMatchesTeamYear,
        ),
        path(
            "api/team_matches/team/<num>/year/<year>/elims",
            team_match_views._TeamMatchesElim,
        ),
        path(
            "api/team_matches/team/<num>/event/<event>",
            team_match_views.TeamMatchesTeamEvent,
        ),
        path(
            "api/team_matches/team/<num>/event/<event>/elims",
            team_match_views._TeamMatchesElim,
        ),
    ]
)

"""YEARS"""
urlpatterns.extend(
    [
        path("api/year/<year>", year_views.Year),
        path("api/years", year_views.Years),
        path("api/years/by/<metric>", year_views.YearsByMetric),
    ]
)

"""EVENTS"""
urlpatterns.extend(
    [
        path("api/event/<event>", event_views.Event),
        path("api/events", event_views.Events),
        path("api/events/by/<metric>", event_views.EventsByMetric),
        path("api/events/country/<country>", event_views._Events),
        path("api/events/country/<country>/by/<metric>", event_views._Events),
        path("api/events/country/<country>/state/<state>", event_views._Events),
        path(
            "api/events/country/<country>/state/<state>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/district/<district>", event_views._Events),
        path("api/events/district/<district>/by/<metric>", event_views._Events),
        path("api/events/type/<type>", event_views._Events),
        path("api/events/type/<type>/by/<metric>", event_views._Events),
        path("api/events/type/<type>/country/<country>", event_views._Events),
        path(
            "api/events/type/<type>/country/<country>/by/<metric>", event_views._Events
        ),
        path(
            "api/events/type/<type>/country/<country>/state/<state>",
            event_views._Events,
        ),
        path(
            "api/events/type/<type>/country/<country>/state/<state>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/type/<type>/district/<district>", event_views._Events),
        path(
            "api/events/type/<type>/district/<district>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/week/<week>", event_views._Events),
        path("api/events/week/<week>/by/<metric>", event_views._Events),
        path("api/events/week/<week>/country/<country>", event_views._Events),
        path(
            "api/events/week/<week>/country/<country>/by/<metric>", event_views._Events
        ),
        path(
            "api/events/week/<week>/country/<country>/state/<state>",
            event_views._Events,
        ),
        path(
            "api/events/week/<week>/country/<country>/state/<state>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/week/<week>/district/<district>", event_views._Events),
        path(
            "api/events/week/<week>/district/<district>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/type/<type>/week/<week>", event_views._Events),
        path("api/events/type/<type>/week/<week>/by/<metric>", event_views._Events),
        path(
            "api/events/type/<type>/week/<week>/country/<country>", event_views._Events
        ),
        path(
            "api/events/type/<type>/week/<week>/country/<country>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/type/<type>/week/<week>/country/<country>/state/<state>",
            event_views._Events,
        ),
        path(
            "api/events/type/<type>/week/<week>/country/<country>/state/<state>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/type/<type>/week/<week>/district/<district>",
            event_views._Events,
        ),
        path(
            "api/events/type/<type>/week/<week>/district/<district>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/year/<year>", event_views.EventsYear),
        path("api/events/year/<year>/by/<metric>", event_views.EventsYearByMetric),
        path("api/events/year/<year>/country/<country>", event_views._Events),
        path(
            "api/events/year/<year>/country/<country>/by/<metric>", event_views._Events
        ),
        path(
            "api/events/year/<year>/country/<country>/state/<state>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/country/<country>/state/<state>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/year/<year>/district/<district>", event_views._Events),
        path(
            "api/events/year/<year>/district/<district>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/year/<year>/type/<type>", event_views._Events),
        path("api/events/year/<year>/type/<type>/by/<metric>", event_views._Events),
        path(
            "api/events/year/<year>/type/<type>/country/<country>", event_views._Events
        ),
        path(
            "api/events/year/<year>/type/<type>/country/<country>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/country/<country>/state/<state>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/country/<country>/state/<state>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/district/<district>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/district/<district>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/year/<year>/week/<week>", event_views._Events),
        path("api/events/year/<year>/week/<week>/by/<metric>", event_views._Events),
        path(
            "api/events/year/<year>/week/<week>/country/<country>", event_views._Events
        ),
        path(
            "api/events/year/<year>/week/<week>/country/<country>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/week/<week>/country/<country>/state/<state>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/week/<week>/country/<country>/state/<state>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/week/<week>/district/<district>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/week/<week>/district/<district>/by/<metric>",
            event_views._Events,
        ),
        path("api/events/year/<year>/type/<type>/week/<week>", event_views._Events),
        path(
            "api/events/year/<year>/type/<type>/week/<week>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/week/<week>/country/<country>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/week/<week>/country/<country>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/week/<week>/country/<country>/state/<state>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/week/<week>/country/<country>/state/<state>/by/<metric>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/week/<week>/district/<district>",
            event_views._Events,
        ),
        path(
            "api/events/year/<year>/type/<type>/week/<week>/district/<district>/by/<metric>",
            event_views._Events,
        ),
    ]
)

"""MATCHES"""
urlpatterns.extend(
    [
        path("api/match/<match>", match_views.Match),
        path("api/matches", match_views.Matches),
        path("api/matches/page/<page>", match_views._Matches),
        path("api/matches/elims", match_views._MatchesElim),
        path("api/matches/elims/page/<page>", match_views._MatchesElim),
        path("api/matches/year/<year>", match_views.MatchesYear),
        path("api/matches/year/<year>/elims", match_views._MatchesElim),
        path("api/matches/year/<year>/page/<page>", match_views._Matches),
        path("api/matches/event/<event>", match_views.MatchesEvent),
        path("api/matches/event/<event>/elims", match_views._MatchesElim),
    ]
)

"""EVENT SIM"""
urlpatterns.extend(
    [
        path("api/event_sim/event/<event>/simple", event_pred_views.QuickSim),
        path("api/event_sim/event/<event>/full", event_pred_views.Sim),
        path(
            "api/event_sim/event/<event>/full/iterations/<iterations>",
            event_pred_views.Sim,
        ),
        path(
            "api/event_sim/event/<event>/index/<index>/simple", event_pred_views.MeanSim
        ),
        path(
            "api/event_sim/event/<event>/index/<index>/full", event_pred_views.IndexSim
        ),
        path(
            "api/event_sim/event/<event>/index/<index>/full/iterations/<iterations>",
            event_pred_views.IndexSim,
        ),
    ]
)

urlpatterns.append(path("api/", include(router.urls)))
