from rest_framework import viewsets, permissions

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
    TeamMatch as TeamMatchModel,
    TeamEvent as TeamEventModel,
    TeamYear as TeamYearModel,
    Team as TeamModel,
    Event as EventModel,
    Year as YearModel,
)

from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello_world(request):
    years = YearModel.objects.all()
    serializer = YearSerializer(years, many=True)
    return Response(serializer.data)


class TeamMatchView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamMatchSerializer
    queryset = TeamMatchModel.objects.all()
    filterset_class = TeamMatchFilterSet


class TeamEventView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamEventSerializer
    queryset = TeamEventModel.objects.all()
    filterset_class = TeamEventFilterSet


class TeamYearView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamYearSerializer
    queryset = TeamYearModel.objects.all()
    filterset_class = TeamYearFilterSet


class TeamView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = TeamSerializer
    queryset = TeamModel.objects.all()
    filterset_class = TeamFilterSet


class EventView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = EventSerializer
    queryset = EventModel.objects.all()
    filterset_class = EventFilterSet


class YearView(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = YearSerializer
    queryset = YearModel.objects.all()
    filterset_class = YearFilterSet


class UserView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


'''API SECTION'''
# syntax: '/api/teams/?team=%(num)s&limit=2000&o=time'


'''TEAM VIEWS'''


@api_view(['GET'])
def Team(request, num):
    teams = TeamModel.objects.all().filter(team=num)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Team_Years(request, num):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(team=num).order_by("year")
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Team_Events(request, num):
    teamEvents = TeamEventModel.objects.all()
    teamEvents = teamEvents.filter(team=num).order_by("time")
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Team_Matches(request, num):
    teamMatches = TeamMatchModel.objects.all()
    teamMatches = teamMatches.filter(team=num).order_by("time")
    serializer = TeamMatchSerializer(teamMatches, many=True)
    return Response(serializer.data)


'''TEAM YEAR VIEWS'''


@api_view(['GET'])
def TeamYear(request, num, year):
    teamYears = TeamYearModel.objects.all()
    teamYears = teamYears.filter(team=num).filter(year=year)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamYear_Events(request, num, year):
    teamEvents = TeamEventModel.objects.all()
    teamEvents = teamEvents.filter(team=num).filter(year=year).order_by("time")
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamYear_Matches(request, num, year):
    teamMatches = TeamMatchModel.objects.all()
    teamMatches = teamMatches.filter(team=num) \
        .filter(year=year).order_by("time")
    serializer = TeamMatchSerializer(teamMatches, many=True)
    return Response(serializer.data)


'''TEAM YEAR EVENT VIEWS'''


@api_view(['GET'])
def TeamYearEvent(request, num, year, event):
    teamEvents = TeamEventModel.objects.all()
    teamEvents = teamEvents.filter(team=num) \
        .filter(year=year).filter(event=event)
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamYearEvent_Matches(request, num, year, event):
    teamMatches = TeamEventModel.objects.all()
    teamMatches = teamMatches.filter(team=num).filter(year=year) \
        .filter(event=event).order_by("time")
    serializer = TeamMatchSerializer(teamMatches, many=True)
    return Response(serializer.data)


'''TEAMS VIEWS'''


@api_view(['GET'])
def Teams(request):
    teams = TeamModel.objects.all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Teams_byElo(request, elo):
    teams = TeamModel.objects.all()
    teams = teams.order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsActive(request):
    teams = TeamModel.objects.all()
    teams = teams.filter(active=1)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsActive_byElo(request, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(active=1).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsDistrict(request, district):
    teams = TeamModel.objects.all()
    teams = teams.filter(district=district)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsDistrict_byElo(request, district, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(district=district).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsDistrictActive(request, district):
    teams = TeamModel.objects.all()
    teams = teams.filter(district=district).filter(active=1)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsDistrictActive_byElo(request, district, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(district=district) \
        .filter(active=1).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsCountry(request, country):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsCountry_byElo(request, country, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsCountryActive(request, country):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).filter(active=1)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsCountryActive_byElo(request, country, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).filter(active=1).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsState(request, country, state):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).filter(state=state)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsState_byElo(request, country, state, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country) \
        .filter(state=state).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsStateActive(request, country, state):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country).filter(state=state).filter(active=1)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def TeamsStateActive_byElo(request, country, state, elo):
    teams = TeamModel.objects.all()
    teams = teams.filter(country=country) \
        .filter(state=state).filter(active=1).order_by("-" + elo)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


'''TEAMS YEARs VIEWS'''


class TeamsYear(RedirectView):
    url = '/api/_team_years/?year=%(year)s&limit=10000'


class TeamsYear_byElo(RedirectView):
    url = '/api/_team_years/?year=%(year)s&limit=10000&o=-%(elo)s'


class TeamsDistrict_Years(RedirectView):
    url = '/api/_team_years/?district=%(district)s&limit=10000'


class TeamsDistrict_Years_byElo(RedirectView):
    url = '/api/_team_years/?district=%(district)s&limit=10000&o=-%(elo)s'


class TeamsDistrictYear(RedirectView):
    url = '/api/_team_years/?year=%(year)s&district=%(district)s&limit=10000'


class TeamsDistrictYear_byElo(RedirectView):
    url = '/api/_team_years/?' \
          'year=%(year)s&district=%(district)s&limit=10000&o=-%(elo)s'


class TeamsCountry_Years(RedirectView):
    url = '/api/_team_years/?country=%(country)s&limit=10000'


class TeamsCountry_Years_byElo(RedirectView):
    url = '/api/_team_years/?country=%(country)s&limit=10000&o=-%(elo)s'


class TeamsCountryYear(RedirectView):
    url = '/api/_team_years/?year=%(year)s&country=%(country)s&limit=10000'


class TeamsCountryYear_byElo(RedirectView):
    url = '/api/_team_years/?' \
          'year=%(year)s&country=%(country)s&limit=10000&o=-%(elo)s'


class TeamsState_Years(RedirectView):
    url = '/api/_team_years/?country=%(country)s&state=%(state)s&limit=10000'


class TeamsState_Years_byElo(RedirectView):
    url = '/api/_team_years/?' \
          'country=%(country)s&state=%(state)s&limit=10000&o=-%(elo)s'


class TeamsStateYear(RedirectView):
    url = '/api/_team_years/?' \
          'year=%(year)s&country=%(country)s&state=%(state)s&limit=10000'


class TeamsStateYear_byElo(RedirectView):
    url = '/api/_team_years/?' \
          'year=%(year)s&country=%(country)s&state=%(state)s&limit=10000&' \
          'o=-%(elo)s'


'''YEAR VIEWS'''


class Year(RedirectView):
    url = '/api/_years/?year=%(year)s'


class YearEvent(RedirectView):
    url = '/api/_events/?year=%(year)s&event=%(event)s'


class Years(RedirectView):
    url = '/api/_years/?limit=100'


'''EVENT VIEWS'''


class Events(RedirectView):
    url = '/api/_events/?limit=10000'


class Events_byElo(RedirectView):
    url = '/api/_events/?limit=10000&o=-%(elo)s'


class EventYear(RedirectView):
    url = '/api/_events/?year=%(year)s&limit=1000'


class EventYear_byElo(RedirectView):
    url = '/api/_events/?year=%(year)s&limit=1000&o=-%(elo)s'
