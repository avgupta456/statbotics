# type: ignore

from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import permissions, viewsets

from backend.settings import CACHE_TIME
from rankings.filters import (
    EventFilterSet,
    MatchFilterSet,
    TeamEventFilterSet,
    TeamFilterSet,
    TeamMatchFilterSet,
    TeamYearFilterSet,
    YearFilterSet,
)
from rankings.models import (
    Event as EventModel,
    Match as MatchModel,
    Team as TeamModel,
    TeamEvent as TeamEventModel,
    TeamMatch as TeamMatchModel,
    TeamYear as TeamYearModel,
    Year as YearModel,
)
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

    @method_decorator(cache_page(CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TeamView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamSerializer
    queryset = TeamModel.objects.all()
    filterset_class = TeamFilterSet

    @method_decorator(cache_page(CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TeamYearView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamYearSerializer
    queryset = TeamYearModel.objects.all()
    filterset_class = TeamYearFilterSet

    @method_decorator(cache_page(CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class EventView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = EventModel.objects.all()
    filterset_class = EventFilterSet

    @method_decorator(cache_page(CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TeamEventView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamEventSerializer
    queryset = TeamEventModel.objects.all()
    filterset_class = TeamEventFilterSet

    @method_decorator(cache_page(CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class MatchView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = MatchSerializer
    queryset = MatchModel.objects.all()
    filterset_class = MatchFilterSet

    @method_decorator(cache_page(CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class TeamMatchView(viewsets.ModelViewSet):
    swagger_schema = None
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMatchSerializer
    queryset = TeamMatchModel.objects.all()
    filterset_class = TeamMatchFilterSet

    @method_decorator(cache_page(CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class UserView(viewsets.ModelViewSet):
    swagger_schema = None
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @method_decorator(cache_page(CACHE_TIME))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
