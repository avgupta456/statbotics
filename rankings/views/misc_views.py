from rest_framework.decorators import api_view
from rest_framework.response import Response

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

from rankings.models import (
    Year as YearModel,
    Team as TeamModel,
    TeamYear as TeamYearModel,
    Event as EventModel,
    TeamEvent as TeamEventModel,
    Match as MatchModel,
    TeamMatch as TeamMatchModel,
)

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


'''API SECTION'''


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
