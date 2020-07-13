from django.urls import path, include
from rest_framework import routers
from rankings import views

# for swagger
from django.conf.urls import url
from rest_framework import permissions

from drf_yasg.views import SwaggerUIRenderer, get_schema_view
from drf_yasg import openapi

<<<<<<< Updated upstream
=======
from rankings.views import (
    model_views,
    team_views,
    team_year_views,
    team_event_views,
    team_match_views,
    year_views,
    event_views,
    match_views,
    event_pred_views,
)


>>>>>>> Stashed changes
SwaggerUIRenderer.template = 'drf-yasg.html'  # monkey-patching is bad :(

schema_view = get_schema_view(
   openapi.Info(
      title="Statbotics.io API",
      default_version='v1',
   ),
   public=True,
   permission_classes=(permissions.AllowAny,)
)

router = routers.DefaultRouter()
router.register(r'_team_matches', views.TeamMatchView, 'team_match')
router.register(r'_team_events', views.TeamEventView, 'team_event')
router.register(r'_team_years', views.TeamYearView, 'team_year')
router.register(r'_teams', views.TeamView, 'team')
router.register(r'_events', views.EventView, 'event')
router.register(r'_years', views.YearView, 'year')

# commented out url patterns still need models
urlpatterns = [
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),

<<<<<<< Updated upstream
    path('api/team/<num>', views.Team),
    path('api/team/<num>/years', views.Team_Years),
    path('api/team/<num>/events', views.Team_Events),
    path('api/team/<num>/matches', views.Team_Matches),

    path('api/team/<num>/year/<year>', views.TeamYear),
    path('api/team/<num>/year/<year>/events', views.TeamYear_Events),
    path('api/team/<num>/year/<year>/matches', views.TeamYear_Matches),

    path('api/team/<num>/year/<year>/event/<event>', views.TeamYearEvent),
    path('api/team/<num>/year/<year>/event/<event>/matches',
         views.TeamYearEvent_Matches),


    path('api/teams', views.Teams),
    path('api/teams/by/<elo>', views.Teams_byElo),
    path('api/teams/active', views.TeamsActive),
    path('api/teams/active/by/<elo>', views.TeamsActive_byElo),

    path('api/teams/district/<district>', views.TeamsDistrict),
    path('api/teams/district/<district>/by/<elo>', views.TeamsDistrict_byElo),
    path('api/teams/district/<district>/active', views.TeamsDistrictActive),
    path('api/teams/district/<district>/active/by/<elo>',
         views.TeamsDistrictActive_byElo),

    path('api/teams/country/<country>', views.TeamsCountry),
    path('api/teams/country/<country>/by/<elo>', views.TeamsCountry_byElo),
    path('api/teams/country/<country>/active', views.TeamsCountryActive),
    path('api/teams/country/<country>/active/by/<elo>',
         views.TeamsCountryActive_byElo),

    path('api/teams/country/<country>/state/<state>', views.TeamsState),
    path('api/teams/country/<country>/state/<state>/by/<elo>',
         views.TeamsState_byElo),
    path('api/teams/country/<country>/state/<state>/active',
         views.TeamsStateActive),
    path('api/teams/country/<country>/state/<state>/active/by/<elo>',
         views.TeamsStateActive_byElo),

    path('api/teams/year/<year>', views.TeamsYear),
    path('api/teams/year/<year>/by/<elo>', views.TeamsYear_byElo),

    path('api/teams/district/<district>/years', views.TeamsDistrict_Years),
    path('api/teams/district/<district>/years/by/<elo>',
         views.TeamsDistrict_Years_byElo),
    path('api/teams/district/<district>/year/<year>',
         views.TeamsDistrict_Year),
    path('api/teams/district/<district>/year/<year>/by/<elo>',
         views.TeamsDistrict_Year_byElo),

    path('api/teams/country/<country>/years', views.TeamsCountry_Years),
    path('api/teams/country/<country>/years/by/<elo>',
         views.TeamsCountry_Years_byElo),
    path('api/teams/country/<country>/year/<year>', views.TeamsCountry_Year),
    path('api/teams/country/<country>/year/<year>/by/<elo>',
         views.TeamsCountry_Year_byElo),

    path('api/teams/country/<country>/state/<state>/years',
         views.TeamsState_Years),
    path('api/teams/country/<country>/state/<state>/years/by/<elo>',
         views.TeamsState_Years_byElo),
    path('api/teams/country/<country>/state/<state>/year/<year>',
         views.TeamsState_Year),
    path('api/teams/country/<country>/state/<state>/year/<year>/by/<elo>',
         views.TeamsState_Year_byElo),

    path('api/years', views.Years),
    path('api/year/<year>', views.Year),

    path('api/events', views.Events),
    path('api/events/by/<elo>', views.Events_byElo),
    path('api/events/year/<year>', views.EventYear),
    path('api/events/year/<year>/by/<elo>', views.EventYear_byElo),
=======
    # Teams
    path('api/team/<num>', team_views.Team),

    path('api/teams', team_views.Teams),
    path('api/teams/', team_views.Teams),
    path('api/teams/by/<metric>', team_views.TeamsByMetric),
    path('api/teams/active', team_views.TeamsActive),
    path('api/teams/active/by/<metric>', team_views.TeamsActiveByMetric),

    path('api/teams/country/<country>', team_views._Teams),
    path('api/teams/country/<country>/by/<metric>', team_views._Teams),
    path('api/teams/country/<country>/active', team_views._TeamsActive),
    path('api/teams/country/<country>/active/by/<metric>', team_views._TeamsActive),  # noqa 502
    path('api/teams/country/<country>/state/<state>', team_views._Teams),
    path('api/teams/country/<country>/state/<state>/by/<metric>', team_views._Teams),  # noqa 502
    path('api/teams/country/<country>/state/<state>/active', team_views._TeamsActive),  # noqa 502
    path('api/teams/country/<country>/state/<state>/active/by/<metric>', team_views._TeamsActive),  # noqa 502
    path('api/teams/district/<district>', team_views._Teams),
    path('api/teams/district/<district>/by/<metric>', team_views._Teams),
    path('api/teams/district/<district>/active', team_views._TeamsActive),
    path('api/teams/district/<district>/active/by/<metric>', team_views._TeamsActive),  # noqa 502



    # TeamYears
    path('api/team_year/team/<num>/year/<year>', team_year_views.TeamYear),

    path('api/team_years/team/<num>', team_year_views.TeamYearsNum),
    path('api/team_years/team/<num>/by/<metric>', team_year_views.TeamYearsNumByMetric),  # noqa 502
    path('api/team_years/year/<year>', team_year_views.TeamYearsYear),
    path('api/team_years/year/<year>/by/<metric>', team_year_views.TeamYearsYearByMetric),  # noqa 502

    path('api/team_years/year/<year>/country/<country>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/year/<year>/country/<country>/by/<metric>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/year/<year>/country/<country>/state/<state>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/year/<year>/country/<country>/state/<state>/by/<metric>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/year/<year>/district/<district>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/year/<year>/district/<district>/by/<metric>', team_year_views._TeamYears),  # noqa 502

    path('api/team_years/', team_year_views.TeamYears),
    path('api/team_years/page/<page>', team_year_views._TeamYears),
    path('api/team_years/by/<metric>', team_year_views.TeamYearsByMetric),
    path('api/team_years/by/<metric>/page/<page>', team_year_views._TeamYears),

    path('api/team_years/country/<country>', team_year_views._TeamYears),
    path('api/team_years/country/<country>/page/<page>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/country/<country>/by/<metric>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/country/<country>/by/<metric>/page/<page>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/country/<country>/state/<state>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/country/<country>/state/<state>/by/<metric>', team_year_views._TeamYears),  # noqa 502
    path('api/team_years/district/<district>', team_year_views._TeamYears),
    path('api/team_years/district/<district>/by/<metric>', team_year_views._TeamYears),  # noqa 502



    # TeamEvents
    path('api/team_event/team/<num>/event/<event>', team_event_views.TeamEvent),  # noqa 502

    path('api/team_events/team/<num>', team_event_views.TeamEventsNum),
    path('api/team_events/team/<num>/by/<metric>', team_event_views.TeamEventsNumByMetric),  # noqa 502

    path('api/team_events/year/<year>', team_event_views.TeamEventsYear),
    path('api/team_events/year/<year>/page/<page>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/by/<metric>', team_event_views.TeamEventsYearByMetric),  # noqa 502
    path('api/team_events/year/<year>/by/<metric>/page/<page>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/country/<country>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/country/<country>/page/<page>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/country/<country>/by/<metric>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/country/<country>/by/<metric>/page/<page>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/country/<country>/state/<state>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/country/<country>/state/<state>/by/<metric>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/district/<district>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/district/<district>/by/<metric>', team_event_views._TeamEvents),  # noqa 502

    path('api/team_events/team/<num>/year/<year>', team_event_views.TeamEventsNumYear),  # noqa 502
    path('api/team_events/team/<num>/year/<year>/by/<metric>', team_event_views.TeamEventsNumYearByMetric),  # noqa 502

    path('api/team_events/event/<event>', team_event_views.TeamEventsEvent),
    path('api/team_events/event/<event>/by/<metric>', team_event_views.TeamEventsEventByMetric),  # noqa 502

    path('api/team_events', team_event_views.TeamEvents),
    path('api/team_events/page/<page>', team_event_views._TeamEvents),
    path('api/team_events/country/<country>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/country/<country>/page/<page>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/country/<country>/state/<state>', team_event_views._TeamEvents),  # noqa 502
    path('api/team_events/district/<district>', team_event_views._TeamEvents),  # noqa 502



    # TeamMatches
    path('api/team_match/team/<num>/match/<match>', team_match_views.TeamMatch),  # noqa 502

    path('api/team_matches', team_match_views.TeamMatches),
    path('api/team_matches/page/<page>', team_match_views._TeamMatches),
    path('api/team_matches/team/<num>', team_match_views.TeamMatchesTeam),
    path('api/team_matches/year/<year>', team_match_views.TeamMatchesYear),
    path('api/team_matches/year/<year>/page/<page>', team_match_views._TeamMatches),  # noqa 502
    path('api/team_matches/event/<event>', team_match_views.TeamMatchesEvent),
    path('api/team_matches/match/<match>', team_match_views.TeamMatchesMatch),
    path('api/team_matches/team/<num>/year/<year>', team_match_views.TeamMatchesTeamYear),  # noqa 502
    path('api/team_matches/team/<num>/event/<event>', team_match_views.TeamMatchesTeamEvent),  # noqa 502



    # Years
    path('api/year/<year>', year_views.Year),

    path('api/years', year_views.Years),
    path('api/years/by/<metric>', year_views.YearsByMetric),



    # Events
    path('api/event/<event>', event_views.Event),

    path('api/events', event_views.Events),
    path('api/events/by/<metric>', event_views.EventsByMetric),
    path('api/events/country/<country>', event_views._Events),
    path('api/events/country/<country>/by/<metric>', event_views._Events),
    path('api/events/country/<country>/state/<state>', event_views._Events),
    path('api/events/country/<country>/state/<state>/by/<metric>', event_views._Events),  # noqa 502
    path('api/events/district/<district>', event_views._Events),
    path('api/events/district/<district>/by/<metric>', event_views._Events),

    path('api/events/year/<year>', event_views.EventsYear),
    path('api/events/year/<year>/by/<metric>', event_views.EventsYearByMetric),
    path('api/events/year/<year>/country/<country>', event_views._Events),
    path('api/events/year/<year>/country/<country>/by/<metric>', event_views._Events),  # noqa 502
    path('api/events/year/<year>/country/<country>/state/<state>', event_views._Events),  # noqa 502
    path('api/events/year/<year>/country/<country>/state/<state>/by/<metric>', event_views._Events),  # noqa 502
    path('api/events/year/<year>/district/<district>', event_views._Events),
    path('api/events/year/<year>/district/<district>/by/<metric>', event_views._Events),  # noqa 502



    # Matches
    path('api/match/<match>', match_views.Match),

    path('api/matches', match_views.Matches),
    path('api/matches/page/<page>', match_views._Matches),
    path('api/matches/year/<year>', match_views.MatchesYear),
    path('api/matches/year/<year>/page/<page>', match_views._Matches),
    path('api/matches/event/<event>', match_views.MatchesEvent),



    # Event Simulation
    path('api/event_sim/event/<event>/simple', event_pred_views.QuickSim),
    path('api/event_sim/event/<event>/full', event_pred_views.Sim),
    path('api/event_sim/event/<event>/full/iterations/<iterations>', event_pred_views.Sim),  # noqa 502
    path('api/event_sim/event/<event>/index/<index>/simple', event_pred_views.MeanSim),  # noqa 502
    path('api/event_sim/event/<event>/index/<index>/full', event_pred_views.IndexSim),  # noqa 502
    path('api/event_sim/event/<event>/index/<index>/full/iterations/<iterations>', event_pred_views.IndexSim),  # noqa 502


>>>>>>> Stashed changes

    path('api/', include(router.urls)),
]
