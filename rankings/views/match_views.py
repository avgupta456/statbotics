from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rankings.models import Match as MatchModel
from rankings.serializers import MatchSerializer


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", MatchSerializer)},
    operation_description="Information for a given match",
)
@api_view(["GET"])
def Match(request, match):
    matches = MatchModel.objects.filter(key=match).all()
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches (WARNING: VERY SLOW)",
)
@api_view(["GET"])
def _Matches(request, year=None, event=None, playoff=None, page=1):
    matches = MatchModel.objects
    if year:
        matches = matches.filter(year=year)
    if event:
        matches = matches.filter(event=event)
    if playoff:
        matches = matches.filter(playoff=playoff)
    matches = matches.all().order_by("time")
    matches = Paginator(matches, 5000).page(page)
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def _MatchesElim(request, year=None, event=None, page=1):
    return _Matches(request._request, year, event, True, page)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches (WARNING: VERY SLOW)",
)
@api_view(["GET"])
def Matches(request):
    return _Matches(request._request)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches from a given year (WARNING: VERY SLOW)",
)
@api_view(["GET"])
def MatchesYear(request, year):
    return _Matches(request._request, year=year)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches from a given event",
)
@api_view(["GET"])
def MatchesEvent(request, event):
    return _Matches(request._request, event=event)
