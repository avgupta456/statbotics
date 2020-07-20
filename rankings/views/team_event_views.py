from django.core.paginator import Paginator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rankings.models import TeamEvent as TeamEventModel
from rankings.serializers import TeamEventSerializer


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR stats for a given team at a given event",
)
@api_view(["GET"])
def TeamEvent(request, num, event):
    teamEvents = TeamEventModel.objects.filter(team=num).filter(event=event).all()
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method="GET", auto_schema=None)
@api_view(["GET"])
def _TeamEvents(
    request,
    num=None,
    year=None,
    event=None,
    country=None,
    state=None,
    district=None,
    type=None,
    week=None,
    metric=None,
    page=1,
):

    teamEvents = TeamEventModel.objects
    if num:
        teamEvents = teamEvents.filter(team=num)
    if year:
        teamEvents = teamEvents.filter(year=year)
    if event:
        teamEvents = teamEvents.filter(event=event)
    if country:
        teamEvents = teamEvents.filter(country=country)
    if state:
        teamEvents = teamEvents.filter(state=state)
    if district:
        teamEvents = teamEvents.filter(district=district)
    if type:
        teamEvents = teamEvents.filter(type=type)
    if week:
        teamEvents = teamEvents.filter(week=week)
    teamEvents = teamEvents.all()
    if metric:
        teamEvents = teamEvents.order_by(metric)
    else:
        teamEvents = teamEvents.order_by("time")
    teamEvents = Paginator(teamEvents, 5000).page(page)
    serializer = TeamEventSerializer(teamEvents, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all (Team, Event) pairs",
)
@api_view(["GET"])
def TeamEvents(request):
    return _TeamEvents(request._request)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events of specified team",
)
@api_view(["GET"])
def TeamEventsNum(request, num):
    return _TeamEvents(request._request, num=num)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events of specified team, "
    + " ordered by metric. Options are '-elo_start',"
    + " '-elo_pre_playoffs', '-elo_end', '-elo_mean',"
    + " '-elo_max', '-elo_diff', '-opr_start',"
    + "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(["GET"])
def TeamEventsNumByMetric(request, num, metric):
    return _TeamEvents(request._request, num=num, metric=metric)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events in a specified year",
)
@api_view(["GET"])
def TeamEventsYear(request, year):
    return _TeamEvents(request._request, year=year)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events in a specified year, "
    + " by metric. Options are '-elo_start',"
    + " '-elo_pre_playoffs', '-elo_end', '-elo_mean',"
    + " '-elo_max', '-elo_diff', '-opr_start',"
    + "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(["GET"])
def TeamEventsYearByMetric(request, year, metric):
    return _TeamEvents(request._request, year=year, metric=metric)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events with specified year, team",
)
@api_view(["GET"])
def TeamEventsNumYear(request, num, year):
    return _TeamEvents(request._request, num=num, year=year)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all events with specified year, team."
    + "Ordered by metric. Options are '-elo_start',"
    + " '-elo_pre_playoffs', '-elo_end', '-elo_mean',"
    + " '-elo_max', '-elo_diff', '-opr_start',"
    + "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(["GET"])
def TeamEventsNumYearByMetric(request, num, year, metric):
    return _TeamEvents(request._request, num=num, year=year, metric=metric)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all teams in an event",
)
@api_view(["GET"])
def TeamEventsEvent(request, event):
    return _TeamEvents(request._request, event=event)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", TeamEventSerializer)},
    operation_description="Elo and OPR for all teams in an event."
    + "Ordered by metric. Options are '-elo_start',"
    + " '-elo_pre_playoffs', '-elo_end', '-elo_mean',"
    + " '-elo_max', '-elo_diff', '-opr_start',"
    + "  '-opr_end', '-ils_1', '-ils_2'",
)
@api_view(["GET"])
def TeamEventsEventByMetric(request, event, metric):
    return _TeamEvents(request._request, event=event, metric=metric)
