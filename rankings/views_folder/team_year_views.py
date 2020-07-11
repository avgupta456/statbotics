from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rankings.serializers import TeamYearSerializer
from rankings.models import TeamYear as TeamYearModel


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR for a given team  in a given year",
)
@api_view(['GET'])
def TeamYear(request, num, year):
    teamYear = TeamYearModel.objects.filter(team=num).filter(year=year).all()
    serializer = TeamYearSerializer(teamYear, many=False)
    return Response(serializer.data)


@swagger_auto_schema(method='GET', auto_schema=None)
@api_view(['GET'])
def _TeamYears(request, num=None, year=None, country=None, state=None, district=None, metric=None):  # noqa 502:
    teamYears = TeamYearModel.objects
    if num is not None:
        teamYears = teamYears.filter(team=num)
    if year is not None:
        teamYears = teamYears.filter(year=year)
    if country is not None:
        teamYears = teamYears.filter(country=country)
    if state is not None:
        teamYears = teamYears.filter(state=state)
    if district is not None:
        teamYears = teamYears.filter(district=district)
    teamYears = teamYears.all()
    if metric is not None:
        teamYears = teamYears.order_by(metric)
    serializer = TeamYearSerializer(teamYears, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR for all (Team, Year) pairs",
)
@api_view(['GET'])
def TeamYears(request):
    return _TeamYears(request)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR for all (Team, Year) pairs, sorted by" +
                          " a given metric. Options are '-elo_start'," +
                          " '-elo_pre_champs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr', '-opr_auto'," +
                          " '-opr_1', '-opr_2', '-opr_endgame'," +
                          " '-opr_fouls', '-opr_no_fouls', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamYearsByMetric(request, metric):
    return _TeamYears(request, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR stats for a given year (all teams)",
)
@api_view(['GET'])
def TeamYearsYear(request, year):
    return _TeamYears(request, year=year)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR stats for a given year (all teams), " +
                          "sorted by a metric. Options are '-elo_start'," +
                          " '-elo_pre_champs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr', '-opr_auto'," +
                          " '-opr_1', '-opr_2', '-opr_endgame'," +
                          " '-opr_fouls', '-opr_no_fouls', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamYearsYearByMetric(request, year, metric):
    return _TeamYears(request, year=year, metric=metric)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR stats for a given team (all years)",
)
@api_view(['GET'])
def TeamYearsNum(request, num):
    return _TeamYears(request, num=num)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("", TeamYearSerializer)},
    operation_description="Elo and OPR stats for a given year (all teams), " +
                          "sorted by a metric. Options are '-elo_start'," +
                          " '-elo_pre_champs', '-elo_end', '-elo_mean'," +
                          " '-elo_max', '-elo_diff', '-opr', '-opr_auto'," +
                          " '-opr_1', '-opr_2', '-opr_endgame'," +
                          " '-opr_fouls', '-opr_no_fouls', '-ils_1', '-ils_2'",
)
@api_view(['GET'])
def TeamYearsNumByMetric(request, num, metric):
    return _TeamYears(request, num=num, metric=metric)
