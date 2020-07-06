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
    teams = TeamModel.objects.all().filter(team=num)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="List of a team's Elo history separated by year",
)
@api_view(['GET'])
def Team_Years(request, num):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(team=num).order_by("year")
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="List of a team's Elo history separated by event",
)
@api_view(['GET'])
def Team_Events(request, num):
    teamEvents = TeamEventModel.objects.all()
    teamEvents = teamEvents.filter(team=num).order_by("time")
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="List of a team's Elo history separated by match",
)
@api_view(['GET'])
def Team_Matches(request, num):
    teamMatches = TeamMatchModel.objects.all()
    teamMatches = teamMatches.filter(team=num).order_by("time")
    serializer = TeamMatchSerializer(teamMatches, many=True)
    return Response(serializer.data)


'''TEAM YEAR VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A team's Elo performance in a given year",
)
@api_view(['GET'])
def TeamYear(request, num, year):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(team=num).filter(year=year)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="A team's Elo performance in a given year, " +
                          "separated by events",
)
@api_view(['GET'])
def TeamYear_Events(request, num, year):
    teamEvents = TeamEventModel.objects.all()
    teamEvents = teamEvents.filter(team=num).filter(year=year).order_by("time")
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="A team's Elo performance in a given year, " +
                          "separated by matches",
)
@api_view(['GET'])
def TeamYear_Matches(request, num, year):
    teamMatches = TeamMatchModel.objects.all()
    teamMatches = teamMatches.filter(team=num) \
        .filter(year=year).order_by("time")
    serializer = TeamMatchSerializer(teamMatches, many=True)
    return Response(serializer.data)


'''TEAM YEAR EVENT VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="A team's Elo performance in a given event",
)
@api_view(['GET'])
def TeamYearEvent(request, num, year, event):
    teamEvents = TeamEventModel.objects.all()
    teamEvents = teamEvents.filter(team=num) \
        .filter(year=year).filter(event=event)
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="A team's Elo performance in a given event, " +
                          "separated by matches",
)
@api_view(['GET'])
def TeamYearEvent_Matches(request, num, year, event):
    teamMatches = TeamEventModel.objects.all()
    teamMatches = teamMatches.filter(team=num).filter(year=year) \
        .filter(event=event).order_by("time")
    serializer = TeamMatchSerializer(teamMatches, many=True)
    return Response(serializer.data)


'''TEAMS VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of all teams and their basic Elo statistics",
)
@api_view(['GET'])
def Teams(request):
    teams = TeamModel.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of all teams and their basic Elo " +
                          "statistics, sorted by descending Elo",
)
@api_view(['GET'])
def Teams_byElo(request, elo):
    teams = TeamModel.objects.all()
    teams = teams.order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of active teams and " +
                          "their basic Elo statistics",
)
@api_view(['GET'])
def TeamsActive(request):
    teams = TeamModel.objects.all()
    teams = teams.filter(active=1)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of active teams and their " +
                          "basic Elo statistics, sorted by descending Elo",
)
@api_view(['GET'])
def TeamsActive_byElo(request, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(active=1).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of all teams and their basic Elo " +
                          "statistics, from a particular district",
)
@api_view(['GET'])
def TeamsDistrict(request, district):
    teams = TeamModel.objects.all()
    teams = teams.filter(district=district)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of all teams and their basic Elo " +
                          "statistics, from a particular district, " +
                          "sorted by descending Elo",
)
@api_view(['GET'])
def TeamsDistrict_byElo(request, district, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(district=district).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of active teams and their basic Elo" +
                          " statistics, from a particular district",
)
@api_view(['GET'])
def TeamsDistrictActive(request, district):
    teams = TeamModel.objects.all()
    teams = teams.filter(district=district).filter(active=1)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of active teams and their basic Elo " +
                          "statistics, from a particular district, " +
                          "sorted by descending Elo",
)
@api_view(['GET'])
def TeamsDistrictActive_byElo(request, district, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(district=district) \
        .filter(active=1).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of all teams and their basic Elo " +
                          "statistics, from a particular country",
)
@api_view(['GET'])
def TeamsCountry(request, country):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of all teams and their basic Elo " +
                          "statistics, from a particular country, " +
                          "sorted by descending Elo",
)
@api_view(['GET'])
def TeamsCountry_byElo(request, country, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of active teams and their basic Elo " +
                          "statistics, from a particular country",
)
@api_view(['GET'])
def TeamsCountryActive(request, country):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).filter(active=1)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of active teams and their basic Elo " +
                          "statistics, from a particular country, " +
                          "sorted by descending Elo",
)
@api_view(['GET'])
def TeamsCountryActive_byElo(request, country, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).filter(active=1).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of all teams and their basic Elo " +
                          "statistics, from a particular state",
)
@api_view(['GET'])
def TeamsState(request, country, state):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).filter(state=state)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of all teams and their basic Elo " +
                          "statistics, from a particular state, " +
                          "sorted by descending Elo",
)
@api_view(['GET'])
def TeamsState_byElo(request, country, state, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country) \
        .filter(state=state).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of active teams and their basic Elo " +
                          "statistics, from a particular state",
)
@api_view(['GET'])
def TeamsStateActive(request, country, state):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).filter(state=state).filter(active=1)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="A list of active teams and their basic Elo " +
                          "statistics, from a particular state, " +
                          "sorted by descending Elo",
)
@api_view(['GET'])
def TeamsStateActive_byElo(request, country, state, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country) \
        .filter(state=state).filter(active=1).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


'''TEAMS YEARs VIEWS'''


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of teams and their basic Elo statistics" +
                          " for a given year",
)
@api_view(['GET'])
def TeamsYear(request, year):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(year=year)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of teams and their basic Elo statistics" +
                          " for a given year, sorted by descending Elo",
)
@api_view(['GET'])
def TeamsYear_byElo(request, year, elo):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(year=year).order_by("-" + elo)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " all year, from a particular district",
)
@api_view(['GET'])
def TeamsDistrict_Years(request, district):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(district=district)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " all year, from a particular district, sorted by" +
                          " descending Elo",
)
@api_view(['GET'])
def TeamsDistrict_Years_byElo(request, district, elo):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(district=district).order_by("-" + elo)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " a particular year, from a particular district",
)
@api_view(['GET'])
def TeamsDistrict_Year(request, year, district):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(year=year).filter(district=district)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " a particular year, from a particular district," +
                          " sorted by descending Elo",
)
@api_view(['GET'])
def TeamsDistrict_Year_byElo(request, year, district, elo):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(year=year) \
        .filter(district=district).order_by("-" + elo)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " all year, from a particular country",
)
@api_view(['GET'])
def TeamsCountry_Years(request, country):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(country=country)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " all year, from a particular country, sorted by" +
                          " descending Elo",
)
@api_view(['GET'])
def TeamsCountry_Years_byElo(request, country, elo):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(country=country).order_by("-" + elo)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " a particular year, from a particular country",
)
@api_view(['GET'])
def TeamsCountry_Year(request, year, country):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(year=year).filter(country=country)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " a particular year, from a particular country," +
                          " sorted by descending Elo",
)
@api_view(['GET'])
def TeamsCountry_Year_byElo(request, year, country, elo):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(year=year) \
        .filter(country=country).order_by("-" + elo)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " all year, from a particular state",
)
@api_view(['GET'])
def TeamsState_Years(request, country, state):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(country=country).filter(state=state)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " all year, from a particular state, sorted by" +
                          " descending Elo",
)
@api_view(['GET'])
def TeamsState_Years_byElo(request, country, state, elo):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(country=country) \
        .filter(state=state).order_by("-" + elo)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " a particular year, from a particular state",
)
@api_view(['GET'])
def TeamsState_Year(request, year, country, state):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(year=year) \
        .filter(country=country).filter(state=state)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="A list of single season team Elos statistics, for" +
                          " a particular year, from a particular state," +
                          " sorted by descending Elo",
)
@api_view(['GET'])
def TeamsState_Year_byElo(request, year, country, state, elo):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(year=year) \
        .filter(country=country).filter(state=state).order_by("-" + elo)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


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

from event_pred import event_pred


@api_view(['GET'])
def EventPred(request):
    print(event_pred.quickSim(2019, "nccmp"))
    return Response()
