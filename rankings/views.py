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
    UserSerializer,
)

from .filters import (
    TeamMatchFilterSet,
    TeamEventFilterSet,
    TeamYearFilterSet,
    TeamFilterSet,
    EventFilterSet,
    YearFilterSet,
)
from .models import (
    TeamMatch,
    TeamEvent,
    TeamYear,
    Team,
    Event,
    Year,
)

from django.contrib.auth.models import User
from django.views.generic.base import RedirectView

class TeamMatchView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMatchSerializer
    queryset = TeamMatch.objects.all()
    filterset_class = TeamMatchFilterSet

class TeamEventView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamEventSerializer
    queryset = TeamEvent.objects.all()
    filterset_class = TeamEventFilterSet

class TeamYearView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamYearSerializer
    queryset = TeamYear.objects.all()
    filterset_class = TeamYearFilterSet

class TeamView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    filterset_class = TeamFilterSet

class EventView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filterset_class = EventFilterSet

class YearView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = YearSerializer
    queryset = Event.objects.all()
    filterset_class = YearFilterSet

class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

'''API SECTION'''
#syntax: '/api/teams/?team=%(num)s&limit=2000&o=time'

class Team(RedirectView):
    url = '/api/teams/?team=%(num)s'
