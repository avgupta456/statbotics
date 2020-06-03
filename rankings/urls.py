from django.urls import path, include
from rest_framework import routers
from rankings import views

router = routers.DefaultRouter()
router.register(r'_team_matches', views.TeamMatchView, 'team_match')
router.register(r'_team_events', views.TeamEventView, 'team_event')
router.register(r'_team_years', views.TeamYearView, 'team_year')
router.register(r'_teams', views.TeamView, 'team')
router.register(r'_events', views.EventView, 'event')
router.register(r'_years', views.YearView, 'year')

# commented out url patterns still need models
urlpatterns = [
    path('api/team/<num>', views.Team.as_view()),

    path('api/team/<num>/years', views.Team_Years.as_view()),

    path('api/team/<num>/events', views.Team_Events.as_view()),

    path('api/team/<num>/matches', views.Team_Matches.as_view()),

    path('api/team/<num>/year/<year>', views.TeamYear.as_view()),

    path('api/team/<num>/year/<year>/events', views.TeamYear_Events.as_view()),

    path('api/team/<num>/year/<year>/matches',
         views.TeamYear_Matches.as_view()),

    path('api/team/<num>/year/<year>/event/<event>',
         views.TeamYearEvent.as_view()),

    path('api/team/<num>/year/<year>/event/<event>/matches',
         views.TeamYearEvent_Matches.as_view()),


    path('api/teams', views.Teams.as_view()),  # automatically adds a /
    path('api/teams/', views.Teams.as_view()),  # better safe then sorry though

    path('api/teams/by/<elo>', views.Teams_byElo.as_view()),

    path('api/teams/active', views.TeamsActive.as_view()),

    path('api/teams/active/by/<elo>', views.TeamsActive_byElo.as_view()),

    path('api/teams/district/<district>', views.TeamsDistrict.as_view()),

    path('api/teams/district/<district>/by/<elo>',
         views.TeamDistrict_byElo.as_view()),

    path('api/teams/district/<district>/active',
         views.TeamsDistrictActive.as_view()),

    path('api/teams/district/<district>/active/by/<elo>',
         views.TeamsDistrictActive_byElo.as_view()),

    path('api/teams/country/<country>', views.TeamsCountry.as_view()),

    path('api/teams/country/<country>/by/<elo>',
         views.TeamsCountry_byElo.as_view()),

    path('api/teams/country/<country>/active',
         views.TeamsCountryActive.as_view()),

    path('api/teams/country/<country>/active/by/<elo>',
         views.TeamsCountryActive_byElo.as_view()),

    path('api/teams/country/<country>/state/<state>',
         views.TeamsState.as_view()),
    path('api/teams/country/<country>/state/<state>/by/<elo>',
         views.TeamsState_byElo.as_view()),
    path('api/teams/country/<country>/state/<state>/active',
         views.TeamsStateActive.as_view()),

    path('api/teams/country/<country>/state/<state>/active/by/<elo>',
         views.TeamsStateActive_byElo.as_view()),

    path('api/teams/year/<year>', views.TeamsYear.as_view()),

    path('api/teams/year/<year>/by/<elo>', views.TeamsYear_byElo.as_view()),

    path('api/teams/district/<district>/years',
         views.TeamsDistrict_Years.as_view()),

    path('api/teams/district/<district>/years/by/<elo>',
         views.TeamsDistrict_Years_byElo.as_view()),

    path('api/teams/district/<district>/year/<year>',
         views.TeamsDistrictYear.as_view()),

    path('api/teams/district/<district>/year/<year>/by/<elo>',
         views.TeamsDistrictYear_byElo.as_view()),

    path('api/teams/country/<country>/years',
         views.TeamsCountry_Years.as_view()),

    path('api/teams/country/<country>/years/by/<elo>',
         views.TeamsCountry_Years_byElo.as_view()),

    path('api/teams/country/<country>/year/<year>',
         views.TeamsCountryYear.as_view()),

    path('api/teams/country/<country>/year/<year>/by/<elo>',
         views.TeamsCountryYear_byElo.as_view()),


    path('api/teams/country/<country>/state/<state>/years',
         views.TeamsState_Years.as_view()),

    path('api/teams/country/<country>/state/<state>/years/by/<elo>',
         views.TeamsState_Years_byElo.as_view()),

    path('api/teams/country/<country>/state/<state>/year/<year>',
         views.TeamsStateYear.as_view()),

    path('api/teams/country/<country>/state/<state>/year/<year>/by/<elo>',
         views.TeamsStateYear_byElo.as_view()),


    path('api/year/<year>', views.Year.as_view()),

    # path('api/year/<year>/matches', views.Year_Matches.as_view()),

    path('api/year/<year>/event/<event>', views.YearEvent.as_view()),

    # path('api/year/<year>/event/<event>/matches',
    # views.YearEvent_Matches.as_view()),

    # path('api/year/<year>/event/<event>/match/<match>',
    # views.YearEventMatch.as_view()),

    path('api/years', views.Years.as_view()),

    path('api/years/', views.Years.as_view()),

    path('api/events/', views.Events.as_view()),

    path('api/events/by/<elo>', views.Events_byElo.as_view()),

    path('api/events/year/<year>', views.EventYear.as_view()),

    path('api/events/year/<year>/by/<elo>', views.EventYear_byElo.as_view()),

    path('api/', include(router.urls)),
]
