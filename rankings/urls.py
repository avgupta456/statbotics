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

    path('api/event_pred', views.EventPred),

    path('api/', include(router.urls)),
]
