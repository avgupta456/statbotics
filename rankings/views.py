from django.shortcuts import render
from rest_framework import viewsets, generics, mixins, permissions, status
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
from .filters import TeamMatchFilterSet
from django.contrib.auth.models import User

class TeamMatchView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMatchSerializer
    queryset = TeamMatch.objects.all()
    filterset_class = TeamMatchFilterSet
    #filterset_fields = ('team', )

    '''
    def get_queryset(self):
       qs = super().get_queryset()
       only_team = str(self.request.query_params.get('team')).lower()
       return qs.filter(team=int(only_team))
    '''

class TeamMatchViewQuery(mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMatchSerializer
    queryset = User.objects.all()

    filterset_fields = ['year', 'event', 'team', 'match']

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
