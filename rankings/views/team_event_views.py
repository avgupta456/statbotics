from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rankings.serializers import TeamEventSerializer
from rankings.models import TeamEvent as TeamEventModel


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
    else:
        teamEvents = teamEvents.order_by('time')
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
