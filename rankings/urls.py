from django.urls import path, include
from rest_framework import routers
from rankings import views

# for swagger
from django.conf.urls import url
from rest_framework import permissions

from drf_yasg.views import SwaggerUIRenderer, get_schema_view
from drf_yasg import openapi

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
router.register(r'_years', views.YearView, 'year')
router.register(r'_teams', views.TeamView, 'team')
router.register(r'_team_years', views.TeamYearView, 'team_year')
router.register(r'_events', views.EventView, 'event')
router.register(r'_team_events', views.TeamEventView, 'team_event')
router.register(r'_matches', views.MatchView, 'match')
router.register(r'_team_matches', views.TeamMatchView, 'team_match')

# commented out url patterns still need models
urlpatterns = [
    url(r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),

    # Teams (17)
    path('api/team/<num>', views.Team),
    path('api/teams', views.Teams),
    path('api/teams/by/<metric>', views.TeamsByMetric),
    path('api/teams/active', views.TeamsActive),
    path('api/teams/active/by/<metric>', views.TeamsActiveByMetric),
    path('api/teams/country/<country>', views._Teams),
    path('api/teams/country/<country>/by/<metric>', views._Teams),
    path('api/teams/country/<country>/active', views._TeamsActive),
    path('api/teams/country/<country>/active/by/<metric>', views._TeamsActive),
    path('api/teams/country/<country>/state/<state>', views._Teams),
    path('api/teams/country/<country>/state/<state>/by/<metric>', views._Teams),  # noqa 502
    path('api/teams/country/<country>/state/<state>/active', views._TeamsActive),  # noqa 502
    path('api/teams/country/<country>/state/<state>/active/by/<metric>', views._TeamsActive),  # noqa 502
    path('api/teams/district/<district>', views._Teams),
    path('api/teams/district/<district>/by/<metric>', views._Teams),
    path('api/teams/district/<district>/active', views._TeamsActive),
    path('api/teams/district/<district>/active/by/<metric>', views._TeamsActive),  # noqa 502

    # TeamYears (19)
    path('api/team_year/team/<num>/year/<year>', views.TeamYear),
    path('api/team_years/team/<num>', views.TeamYearsNum),
    path('api/team_years/team/<num>/by/<metric>', views.TeamYearsNumByMetric),
    path('api/team_years/year/<year>', views.TeamYearsYear),
    path('api/team_years/year/<year>/by/<metric>', views.TeamYearsYearByMetric),  # noqa 502
    path('api/team_years/year/<year>/country/<country>', views._TeamYears),
    path('api/team_years/year/<year>/country/<country>/by/<metric>', views._TeamYears),  # noqa 502
    path('api/team_years/year/<year>/country/<country>/state/<state>', views._TeamYears),  # noqa 502
    path('api/team_years/year/<year>/country/<country>/state/<state>/by/<metric>', views._TeamYears),  # noqa 502
    path('api/team_years/year/<year>/district/<district>', views._TeamYears),
    path('api/team_years/year/<year>/district/<district>/by/<metric>', views._TeamYears),  # noqa 502
    path('api/team_years', views.TeamYears),
    path('api/team_years/by/<metric>', views.TeamYearsByMetric),
    path('api/team_years/country/<country>', views._TeamYears),
    path('api/team_years/country/<country>/by/<metric>', views._TeamYears),
    path('api/team_years/country/<country>/state/<state>', views._TeamYears),
    path('api/team_years/country/<country>/state/<state>/by/<metric>', views._TeamYears),  # noqa 502
    path('api/team_years/district/<district>', views._TeamYears),
    path('api/team_years/district/<district>/by/<metric>', views._TeamYears),

    # TeamEvents (15)
    path('api/team_event/team/<num>/event/<event>', views.TeamEvent),
    path('api/team_events/team/<num>', views.TeamEventsNum),
    path('api/team_events/team/<num>/by/<metric>', views.TeamEventsNumByMetric),  # noqa 502
    path('api/team_events/year/<year>', views.TeamEventsYear),
    path('api/team_events/year/<year>/by/<metric>', views.TeamEventsYearByMetric),  # noqa 502
    path('api/team_events/year/<year>/country/<country>', views._TeamEvents),
    path('api/team_events/year/<year>/country/<country>/by/<metric>', views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/country/<country>/state/<state>', views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/country/<country>/state/<state>/by/<metric>', views._TeamEvents),  # noqa 502
    path('api/team_events/year/<year>/district/<district>', views._TeamEvents),
    path('api/team_events/year/<year>/district/<district>/by/<metric>', views._TeamEvents),  # noqa 502
    path('api/team_events/team/<num>/year/<year>', views.TeamEventsNumYear),
    path('api/team_events/team/<num>/year/<year>/by/<metric>', views.TeamEventsNumYearByMetric),  # noqa 502
    path('api/team_events/event/<event>', views.TeamEventsEvent),
    path('api/team_events/event/<event>/by/<metric>', views.TeamEventsEventByMetric),  # noqa 502
    path('api/team_events', views.TeamEvents),
    path('api/team_events/by/<metric>', views.TeamEventsByMetric),

    # TeamMatches
    path('api/team_match/team/<team>/match/<match>', views.TeamMatch),
    path('api/team_matches', views.TeamMatches),
    path('api/team_matches/team/<team>', views.TeamMatchesTeam),
    path('api/team_matches/year/<year>', views.TeamMatchesYear),
    path('api/team_matches/event/<event>', views.TeamMatchesEvent),
    path('api/team_matches/match/<match>', views.TeamMatchesMatch),
    path('api/team_matches/team/<team>/year/<year>', views.TeamMatchesTeamYear),  # noqa 502
    path('api/team_matches/team/<team>/event/<event>', views.TeamMatchesTeamEvent),  # noqa 502


    path('api/event_pred', views.EventPred),

    path('api/', include(router.urls)),
]
