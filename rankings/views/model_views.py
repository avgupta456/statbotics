from django.contrib.auth.models import User

from rest_framework import viewsets, permissions

from rankings.serializers import (
    YearSerializer,
    TeamSerializer,
    TeamYearSerializer,
    EventSerializer,
    TeamEventSerializer,
    MatchSerializer,
    TeamMatchSerializer,
    UserSerializer
)

from rankings.filters import (
    YearFilterSet,
    TeamFilterSet,
    TeamYearFilterSet,
    EventFilterSet,
    TeamEventFilterSet,
    MatchFilterSet,
    TeamMatchFilterSet,
)

from rankings.models import (
    Year as YearModel,
    Team as TeamModel,
    TeamYear as TeamYearModel,
    Event as EventModel,
    TeamEvent as TeamEventModel,
    Match as MatchModel,
    TeamMatch as TeamMatchModel,
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
