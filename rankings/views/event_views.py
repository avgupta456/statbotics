from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rankings.models import Event as EventModel
from rankings.serializers import EventSerializer


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", EventSerializer)},
    operation_description="Basic information and stats for specified event",
)
@api_view(["GET"])
def Event(request, event):
    events = EventModel.objects.filter(key=event).all()
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@swagger_auto_schema(method="GET", auto_schema=None)
@api_view(["GET"])
def _Events(
    request,
    year=None,
    country=None,
    state=None,
    district=None,
    type=None,
    week=None,
    metric=None,
):

    events = EventModel.objects
    if year is not None:
        events = events.filter(year=year)
    if country is not None:
        events = events.filter(country=country)
    if state is not None:
        events = events.filter(state=state)
    if district is not None:
        events = events.filter(district=district)
    if type is not None:
        events = events.filter(type=type)
    if week is not None:
        events = events.filter(week=week)
    events = events.all()
    if metric is not None:
        events = events.order_by(metric)
    else:
        events = events.order_by("time")
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", EventSerializer)},
    operation_description="Basic information and stats for all event",
)
@api_view(["GET"])
def Events(request):
    return _Events(request._request)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", EventSerializer)},
    operation_description="Basic information and stats for all event,"
    + " ordered by metric. Options are '-elo_top8',"
    + " '-elo_top24', '-elo_mean', '-opr_top8',"
    + " '-opr_top24', '-opr_mean'",
)
@api_view(["GET"])
def EventsByMetric(request, metric):
    return _Events(request._request, metric=metric)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", EventSerializer)},
    operation_description="Basic information and stats for all event in a given year",
)
@api_view(["GET"])
def EventsYear(request, year):
    return _Events(request._request, year=year)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", EventSerializer)},
    operation_description="Basic information and stats for all event in a given year,"
    + " ordered by metric. Options are '-elo_top8',"
    + " '-elo_top24', '-elo_mean', '-opr_top8',"
    + " '-opr_top24', '-opr_mean'",
)
@api_view(["GET"])
def EventsYearByMetric(request, year, metric):
    return _Events(request._request, year=year, metric=metric)
