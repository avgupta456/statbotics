from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .serializers import (
    TeamMatchSerializer,
    TeamEventSerializer,
    TeamYearSerializer,
    TeamSerializer,
    EventSerializer,
    YearSerializer,
    UserSerializer
)

from .models import TeamMatch, TeamEvent, TeamYear, Team, Event, Year
from django.contrib.auth.models import User

from .filters import TeamMatchFilterSet

from django.views.generic.base import RedirectView

class TeamMatchView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMatchSerializer
    queryset = TeamMatch.objects.all()
    filterset_class = TeamMatchFilterSet

class TeamRedirect(RedirectView):
    url = '/api/team_matches/?team=%(num)s&limit=2000'

class TeamEventView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamEventSerializer
    queryset = TeamEvent.objects.all()

class TeamYearView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamYearSerializer
    queryset = TeamYear.objects.all()

class TeamView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()

class EventView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()

class YearView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = YearSerializer
    queryset = Event.objects.all()

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
