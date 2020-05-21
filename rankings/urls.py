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
    path('api/teams/<num>', views.Team.as_view()),
    path('api/', include(router.urls)),
]
