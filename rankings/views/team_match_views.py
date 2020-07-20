from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rankings.models import TeamMatch as TeamMatchModel
from rankings.serializers import TeamMatchSerializer


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for a specific (Team, Match) pair",
)
@api_view(["GET"])
def TeamMatch(request, num, match):
    teamMatch = TeamMatchModel.objects.filter(team=num).filter(match=match).all()
    serializer = TeamMatchSerializer(teamMatch, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method="GET", auto_schema=None)
@api_view(["GET"])
def _TeamMatches(
    request, num=None, year=None, event=None, match=None, playoff=None, page=1
):

    teamMatches = TeamMatchModel.objects
    if num:
        teamMatches = teamMatches.filter(team=num)
    if year:
        teamMatches = teamMatches.filter(year=year)
    if event:
        teamMatches = teamMatches.filter(event=event)
    if match:
        teamMatches = teamMatches.filter(match=match)
    if playoff:
        teamMatches = teamMatches.filter(playoff=playoff)
    teamMatches = Paginator(teamMatches.all().order_by("time"), 5000).page(page)
    serializer = TeamMatchSerializer(teamMatches, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def _TeamMatchesElim(request, num=None, year=None, event=None, match=None, page=1):
    return _TeamMatches(request._request, num, year, event, match, True, page)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for all (Team, Match) pairs",
)
@api_view(["GET"])
def TeamMatches(request):
    return _TeamMatches(request._request)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified team",
)
@api_view(["GET"])
def TeamMatchesTeam(request, num):
    return _TeamMatches(request._request, num=num)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified year",
)
@api_view(["GET"])
def TeamMatchesYear(request, year):
    return _TeamMatches(request._request, year=year)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified event",
)
@api_view(["GET"])
def TeamMatchesEvent(request, event):
    return _TeamMatches(request._request, event=event)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified match",
)
@api_view(["GET"])
def TeamMatchesMatch(request, match):
    return _TeamMatches(request._request, match=match)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified team, year",
)
@api_view(["GET"])
def TeamMatchesTeamYear(request, num, year):
    return _TeamMatches(request._request, num=num, year=year)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamMatchSerializer)},
    operation_description="Statistics for (Team, Match) pairs with specified team, event",
)
@api_view(["GET"])
def TeamMatchesTeamEvent(request, num, event):
    return _TeamMatches(request._request, num=num, event=event)
