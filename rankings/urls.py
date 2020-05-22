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

#commented out url patterns still need models
urlpatterns = [
    path('api/team/<num>', views.Team.as_view()),
    path('api/team/<num>/years', views.Team_Years.as_view()),
    path('api/team/<num>/events', views.Team_Events.as_view()),
    path('api/team/<num>/matches', views.Team_Matches.as_view()),
    path('api/team/<num>/year/<year>', views.TeamYear.as_view()),
    path('api/team/<num>/year/<year>/events', views.TeamYear_Events.as_view()),
    path('api/team/<num>/year/<year>/matches', views.TeamYear_Matches.as_view()),
    path('api/team/<num>/year/<year>/event/<event>', views.TeamYearEvent.as_view()),
    path('api/team/<num>/year/<year>/event/<event>/matches', views.TeamYearEvent_Matches.as_view()),
    path('api/teams', views.Teams.as_view()), #automatically adds a / on Chrome
    path('api/teams/', views.Teams.as_view()), #better safe then sorry though
    path('api/teams/by/<elo>', views.Teams_byElo.as_view()),
    path('api/teams/active', views.TeamsActive.as_view()),
    path('api/teams/active/by/<elo>', views.TeamsActive_byElo.as_view()),
    path('api/teams/district/<district>', views.TeamsDistrict.as_view()),
    path('api/teams/district/<district>/by/<elo>', views.TeamDistrict_byElo.as_view()),
    path('api/teams/district/<district>/active', views.TeamsDistrictActive.as_view()),
    path('api/teams/district/<district>/active/by/<elo>', views.TeamsDistrictActive_byElo.as_view()),
    path('api/teams/region/<region>', views.TeamsRegion.as_view()),
    path('api/teams/region/<region>/by/<elo>', views.TeamsRegion_byElo.as_view()),
    path('api/teams/region/<region>/active', views.TeamsRegionActive.as_view()),
    path('api/teams/region/<region>/active/by/<elo>', views.TeamsRegionActive_byElo.as_view()),
    path('api/teams/year/<year>', views.TeamsYear.as_view()),
    path('api/teams/year/<year>/by/<elo>', views.TeamsYear_byElo.as_view()),
    path('api/teams/year/<year>/district/<district>', views.TeamsYearDistrict.as_view()),
    path('api/teams/year/<year>/district/<district>/by/<elo>', views.TeamsYearDistrict_byElo.as_view()),
    path('api/teams/year/<year>/region/<region>', views.TeamsYearRegion.as_view()),
    path('api/teams/year/<year>/region/<region>/by/<elo>', views.TeamsYearRegion_byElo.as_view()),
    path('api/year/<year>', views.Year.as_view()),
    #path('api/year/<year>/matches', views.Year_Matches.as_view()),
    path('api/year/<year>/event/<event>', views.YearEvent.as_view()),
    #path('api/year/<year>/event/<event>/matches', views.YearEvent_Matches.as_view()),
    #path('api/year/<year>/event/<event>/match/<match>', views.YearEventMatch.as_view()),
    path('api/years', views.Years.as_view()),
    path('api/years/', views.Years.as_view()),
    path('api/events/', views.Events.as_view()),
    path('api/events/by/<elo>', views.Events_byElo.as_view()),
    path('api/events/year/<year>', views.EventYear.as_view()),
    path('api/events/year/<year>/by/<elo>', views.EventYear_byElo.as_view()),
    path('api/', include(router.urls)),
]
