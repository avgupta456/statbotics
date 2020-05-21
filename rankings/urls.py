from django.urls import path, include
from rest_framework import routers
from rankings import views

router = routers.DefaultRouter()
router.register(r'team_matches', views.TeamMatchView, 'team_match')
router.register(r'team_events', views.TeamEventView, 'team_event')
router.register(r'team_years', views.TeamYearView, 'team_year')
router.register(r'teams', views.TeamView, 'team')
router.register(r'events', views.EventView, 'event')
router.register(r'years', views.YearView, 'year')

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
    path('api/', include(router.urls)),
]
