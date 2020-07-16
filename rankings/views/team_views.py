from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rankings.serializers import TeamSerializer
from rankings.models import Team as TeamModel


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description='Basic information and Elo summary for a team',
)
@api_view(['GET'])
def Team(request, num):
    teams = TeamModel.objects.filter(team=num).all()
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def _Teams(request, metric=None, country=None, state=None, district=None, active=None):  # noqa 502
    teams = TeamModel.objects
    if country:
        teams = teams.filter(country=country)
    if state:
        teams = teams.filter(state=state)
    if district:
        teams = teams.filter(district=district)
    if active:
        teams = teams.filter(active=1)
    teams = teams.all()
    if metric:
        teams = teams.order_by(metric)
    serializer = TeamSerializer(teams, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def _TeamsActive(request, metric=None, country=None, state=None, district=None):  # noqa 502
    return _Teams(request._request, metric, country, state, district, active=1)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="Returns a list of all teams and their statistics",
)
@api_view(['GET'])
def Teams(request):
    return _Teams(request._request)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="Returns a list of all teams, sorted by a metric. " +
                          "Options are '-elo', '-elo_recent', '-elo_mean', " +
                          "and '-elo_max'",
)
@api_view(['GET'])
def TeamsByMetric(request, metric):
    return _Teams(request._request, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="Returns a list of active teams and their statistics.",  # noqa 502
)
@api_view(['GET'])
def TeamsActive(request):
    return _Teams(request._request, active=1)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamSerializer)},
    operation_description="Returns a list of active teams, sorted by a " +
                          "metric. Options are '-elo', '-elo_recent', " +
                          "'-elo_mean', and '-elo_max'",
)
@api_view(['GET'])
def TeamsActiveByMetric(request, metric):
    return _Teams(request._request, metric=metric, active=1)
