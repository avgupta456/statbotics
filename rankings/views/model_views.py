from django.contrib.auth.models import User
from rest_framework import permissions, viewsets

from rankings.filters import (
    EventFilterSet,
    MatchFilterSet,
    TeamEventFilterSet,
    TeamFilterSet,
    TeamMatchFilterSet,
    TeamYearFilterSet,
    YearFilterSet,
)
from rankings.models import Event as EventModel
from rankings.models import Match as MatchModel
from rankings.models import Team as TeamModel
from rankings.models import TeamEvent as TeamEventModel
from rankings.models import TeamMatch as TeamMatchModel
from rankings.models import TeamYear as TeamYearModel
from rankings.models import Year as YearModel
from rankings.serializers import (
    EventSerializer,
    MatchSerializer,
    TeamEventSerializer,
    TeamMatchSerializer,
    TeamSerializer,
    TeamYearSerializer,
    UserSerializer,
    YearSerializer,
)


class YearView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = YearSerializer
    queryset = YearModel.objects.all()
    filterset_class = YearFilterSet


class TeamView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamSerializer
    queryset = TeamModel.objects.all()
    filterset_class = TeamFilterSet


class TeamYearView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamYearSerializer
    queryset = TeamYearModel.objects.all()
    filterset_class = TeamYearFilterSet


class EventView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = EventModel.objects.all()
    filterset_class = EventFilterSet


class TeamEventView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamEventSerializer
    queryset = TeamEventModel.objects.all()
    filterset_class = TeamEventFilterSet


class MatchView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MatchSerializer
    queryset = MatchModel.objects.all()
    filterset_class = MatchFilterSet


class TeamMatchView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMatchSerializer
    queryset = TeamMatchModel.objects.all()
    filterset_class = TeamMatchFilterSet


class UserView(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class = UserSerializer
    queryset = User.objects.all()
