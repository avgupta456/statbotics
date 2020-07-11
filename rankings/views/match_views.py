from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rankings.serializers import MatchSerializer
from rankings.models import Match as MatchModel


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="Information for a given match",
)
@api_view(['GET'])
def Match(request, match):
    matches = MatchModel.objects.filter(match=match).all()
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches (WARNING: VERY SLOW)",
)
@api_view(['GET'])
def Matches(request):
    matches = MatchModel.objects.all().order_by('time')
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches from a given year (WARNING: VERY SLOW)",  # noqa 502
)
@api_view(['GET'])
def MatchesYear(request, year):
    matches = MatchModel.objects.filter(year=year).all().order_by('time')
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", MatchSerializer)},
    operation_description="List of all matches from a given event",
)
@api_view(['GET'])
def MatchesEvent(request, event):
    matches = MatchModel.objects.filter(event=event).all().order_by('time')
    serializer = MatchSerializer(matches, many=True)
    return Response(serializer.data)
