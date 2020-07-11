from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import (
    YearSerializer,
    TeamSerializer,
    TeamYearSerializer,
    EventSerializer,
    TeamEventSerializer,
    MatchSerializer,
    TeamMatchSerializer,
    UserSerializer
)

from .filters import (
    YearFilterSet,
    TeamFilterSet,
    TeamYearFilterSet,
    EventFilterSet,
    TeamEventFilterSet,
    MatchFilterSet,
    TeamMatchFilterSet,
)

from .models import (
    Year as YearModel,
    Team as TeamModel,
    TeamYear as TeamYearModel,
    Event as EventModel,
    TeamEvent as TeamEventModel,
    Match as MatchModel,
    TeamMatch as TeamMatchModel,
)

from django.contrib.auth.models import User

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


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


'''API SECTION'''
# syntax: '/api/teams/?team=%(num)s&limit=2000&o=time'


'''TEAM VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description='Basic information and Elo summary for a team',
)
@api_view(['GET'])
def Team(request, num):
    team = TeamModel.objects.filter(team=num).all()
    serializer = TeamSerializer(team, many=False)
    return Response(serializer.data)


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def _Teams(request, metric=None, country=None, state=None, district=None, active=None):  # noqa 502
    teams = TeamModel.objects
    if country is not None:
        teams = teams.filter(country=country)
    if state is not None:
        teams = teams.filter(state=state)
    if district is not None:
        teams = teams.filter(district=district)
    if active is not None:
        teams = teams.filter(active=1)
    teams = teams.all()
    if metric is not None:
        teams = teams.order_by(metric)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def _TeamsActive(request, metric=None, country=None, state=None, district=None):  # noqa 502
    return _Teams(request, metric, country, state, district, active=1)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="Returns a list of all teams and their statistics",
)
@api_view(['GET'])
def Teams(request):
    return _Teams(request)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="Returns a list of all teams, sorted by a metric. " +
                          "Options are '-elo', '-elo_recent', '-elo_mean', " +
                          "and '-elo_max'",
)
@api_view(['GET'])
def TeamsByMetric(request, metric):
    return _Teams(request, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="Returns a list of active teams and their statistics.",  # noqa 502
)
@api_view(['GET'])
def TeamsActive(request):
    return _Teams(request, active=1)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="Returns a list of active teams, sorted by a " +
                          "metric. Options are '-elo', '-elo_recent', " +
                          "'-elo_mean', and '-elo_max'",
)
@api_view(['GET'])
def TeamsActiveByMetric(request, metric):
    return _Teams(request, metric=metric, active=1)


'''TEAM YEAR VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR for a given team  in a given year",
)
@api_view(['GET'])
def TeamYear(request, num, year):
    teamYear = TeamYearModel.objects.filter(team=num).filter(year=year).all()
    serializer = TeamYearSerializer(teamYear, many=False)
    return Response(serializer.data)


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def _TeamYears(request, num=None, year=None, country=None, state=None, district=None, metric=None):  # noqa 502:
    teamYears = TeamYearModel.objects
    if num is not None:
        teamYears = teamYears.filter(team=num)
    if year is not None:
        teamYears = teamYears.filter(year=year)
    if country is not None:
        teamYears = teamYears.filter(country=country)
    if state is not None:
        teamYears = teamYears.filter(state=state)
    if district is not None:
        teamYears = teamYears.filter(district=district)
    teamYears = teamYears.all()
    if metric is not None:
        teamYears = teamYears.order_by(metric)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR for all (Team, Year) pairs",
)
@api_view(['GET'])
def TeamYears(request):
    return _TeamYears(request)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR for all (Team, Year) pairs, sorted by" +
                          " a given metric. Options are '-elo_start'," +
                          " '-elo_pre_champs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr', '-opr_auto'," +
                          " '-opr_1', '-opr_2', '-opr_endgame'," +
                          " '-opr_fouls', '-opr_no_fouls', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamYearsByMetric(request, metric):
    return _TeamYears(request, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR stats for a given year (all teams)",
)
@api_view(['GET'])
def TeamYearsYear(request, year):
    return _TeamYears(request, year=year)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR stats for a given year (all teams), " +
                          "sorted by a metric. Options are '-elo_start'," +
                          " '-elo_pre_champs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr', '-opr_auto'," +
                          " '-opr_1', '-opr_2', '-opr_endgame'," +
                          " '-opr_fouls', '-opr_no_fouls', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamYearsYearByMetric(request, year, metric):
    return _TeamYears(request, year=year, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR stats for a given team (all years)",
)
@api_view(['GET'])
def TeamYearsNum(request, num):
    return _TeamYears(request, num=num)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR stats for a given year (all teams), " +
                          "sorted by a metric. Options are '-elo_start'," +
                          " '-elo_pre_champs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr', '-opr_auto'," +
                          " '-opr_1', '-opr_2', '-opr_endgame'," +
                          " '-opr_fouls', '-opr_no_fouls', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamYearsNumByMetric(request, num, metric):
    return _TeamYears(request, num=num, metric=metric)


'''TEAM EVENT VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR stats for a given team at a given event",  # noqa 502
)
@api_view(['GET'])
def TeamEvent(request, num, event):
    teamEvent = TeamEventModel.objects.filter(team=num).filter(event=event).all()  # noqa 502
    serializer = TeamEventSerializer(teamEvent, many=False)
    return Response(serializer.data)


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def _TeamEvents(request, num=None, year=None, event=None,
                country=None, state=None, district=None, metric=None):
    teamEvents = TeamEventModel.objects
    if num is not None:
        teamEvents = teamEvents.filter(team=num)
    if year is not None:
        teamEvents = teamEvents.filter(year=year)
    if event is not None:
        teamEvents = teamEvents.filter(event=event)
    if country is not None:
        teamEvents = teamEvents.filter(country=country)
    if state is not None:
        teamEvents = teamEvents.filter(state=state)
    if district is not None:
        teamEvents = teamEvents.filter(district=district)
    teamEvents = teamEvents.all()
    if metric is not None:
        teamEvents = teamEvents.order_by(metric)
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all (Team, Event) pairs",
)
@api_view(['GET'])
def TeamEvents(request):
    return _TeamEvents(request)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all (Team, Event) pairs, ordered" +
                          " by metric. Options are '-elo_start'," +
                          " '-elo_pre_playoffs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr_start'," +
                          "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamEventsByMetric(request, metric):
    return _TeamEvents(request, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events of specified team",
)
@api_view(['GET'])
def TeamEventsNum(request, num):
    return _TeamEvents(request, num=num)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events of specified team, " +
                          " ordered by metric. Options are '-elo_start'," +
                          " '-elo_pre_playoffs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr_start'," +
                          "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamEventsNumByMetric(request, num, metric):
    return _TeamEvents(request._request, num=num, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events in a specified year",
)
@api_view(['GET'])
def TeamEventsYear(request, year):
    return _TeamEvents(request, year=year)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events in a specified year, " +
                          " by metric. Options are '-elo_start'," +
                          " '-elo_pre_playoffs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr_start'," +
                          "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamEventsYearByMetric(request, year, metric):
    return _TeamEvents(request, year=year, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events with specified year, team",  # noqa 502
)
@api_view(['GET'])
def TeamEventsNumYear(request, num, year):
    return _TeamEvents(request, num=num, year=year)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events with specified year, team." +  # noqa 502
                          "Ordered by metric. Options are '-elo_start'," +
                          " '-elo_pre_playoffs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr_start'," +
                          "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamEventsNumYearByMetric(request, num, year, metric):
    return _TeamEvents(request, num=num, year=year, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all teams in an event",
)
@api_view(['GET'])
def TeamEventsEvent(request, event):
    return _TeamEvents(request, event=event)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all teams in an event." +
                          "Ordered by metric. Options are '-elo_start'," +
                          " '-elo_pre_playoffs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr_start'," +
                          "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamEventsEventByMetric(request, event, metric):
    return _TeamEvents(request, event=event, metric=metric)


'''TEAM MATCH VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for a specific (Team, Match) pair",
)
@api_view(['GET'])
def TeamMatch(request, num, match):
    teamMatch = TeamMatchModel.objects.filter(team=num).filter(match=match).all()  # noqa 502
    serializer = TeamMatchSerializer(teamMatch, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def _TeamMatches(request, num=None, year=None, event=None, match=None):
    teamMatches = TeamMatchModel.objects
    if num is not None:
        teamMatches = teamMatches.filter(team=num)
    if year is not None:
        teamMatches = teamMatches.filter(year=year)
    if event is not None:
        teamMatches = teamMatches.filter(event=event)
    if match is not None:
        teamMatches = teamMatches.filter(match=match)
    teamMatches = teamMatches.all().order_by("time")
    serializer = TeamMatchSerializer(teamMatches, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for all (Team, Match) pairs",
)
@api_view(['GET'])
def TeamMatches(request):
    return _TeamMatches(request._request)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified team",  # noqa 502
)
@api_view(['GET'])
def TeamMatchesTeam(request, num):
    return _TeamMatches(request._request, num=num)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified year",  # noqa 502
)
@api_view(['GET'])
def TeamMatchesYear(request, year):
    return _TeamMatches(request._request, year=year)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified event",  # noqa 502
)
@api_view(['GET'])
def TeamMatchesEvent(request, event):
    return _TeamMatches(request._request, event=event)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified match",  # noqa 502
)
@api_view(['GET'])
def TeamMatchesMatch(request, match):
    return _TeamMatches(request._request, match=match)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified team, year",  # noqa 502
)
@api_view(['GET'])
def TeamMatchesTeamYear(request, team, year):
    return _TeamMatches(request._request, num=team, year=year)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified team, event",  # noqa 502
)
@api_view(['GET'])
def TeamMatchesTeamEvent(request, team, event):
    return _TeamMatches(request._request, num=team, event=event)


'''YEAR VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", YearSerializer)},
    operation_description="A list of years and their aggregate Elo statistics",
)
@api_view(['GET'])
def Years(request):
    years = YearModel.objects.all()
    serializer = YearSerializer(years, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", YearSerializer)},
    operation_description="Aggregate Elo statistics for a particular year",
)
@api_view(['GET'])
def Year(request, year):
    years = YearModel.objects.all()
    years = years.filter(year=year)
    serializer = YearSerializer(years, many=True)
    return Response(serializer.data)


'''EVENT VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", EventSerializer)},
    operation_description="A list of events and their aggregate " +
                          "Elo statistics",
)
@api_view(['GET'])
def Events(request):
    events = EventModel.objects.all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", EventSerializer)},
    operation_description="A list of events and their aggregate " +
                          "Elo statistics, sorted by descending Elo",
)
@api_view(['GET'])
def Events_byElo(request, elo):
    events = EventModel.objects.all()
    events = events.order_by("-" + elo)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", EventSerializer)},
    operation_description="A list of events and their aggregate " +
                          "Elo statistics, for a given year",
)
@api_view(['GET'])
def EventYear(request, year):
    events = EventModel.objects.all()
    events = events.filter(year=year)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", EventSerializer)},
    operation_description="A list of events and their aggregate " +
                          "Elo statistics, for a given year, sorted by " +
                          "descending Elo",
)
@api_view(['GET'])
def EventYear_byElo(request, year, elo):
    events = EventModel.objects.all()
    events = events.filter(year=year).order_by("-" + elo)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


'''
EVENT PRED (TEMPORARY)
'''

import datetime
from rankings.event_pred import event_pred


@api_view(['GET'])
def EventPred(request):
    start = datetime.datetime.now()
    predictions = event_pred.quickSim(2019, "nccmp")
    end = datetime.datetime.now()
    print(end-start)
    return Response(predictions)
