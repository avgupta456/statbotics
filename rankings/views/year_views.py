from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response

from rankings.models import Year as YearModel
from rankings.serializers import YearSerializer


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", YearSerializer)},
    operation_description="Basic information and prediction stats for given year",
)
@api_view(["GET"])
def Year(request, year):
    years = YearModel.objects.filter(year=year).all()
    serializer = YearSerializer(years, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", YearSerializer)},
    operation_description="Basic information and prediction stats for all year 2002-Present",
)
@api_view(["GET"])
def Years(request):
    years = YearModel.objects.all()
    serializer = YearSerializer(years, many=True)
    return Response(serializer.data)


@swagger_auto_schema(
    method="GET",
    responses={200: openapi.Response("", YearSerializer)},
    operation_description="Basic information and prediction stats for all"
    + " years 2002-Present, ordered by metric. Option"
    + " are '-elo_acc', '-elo_mse', '-opr_acc',"
    + " '-opr_mse', '-mix_acc', '-mix_mse'",
)
@api_view(["GET"])
def YearsByMetric(request, metric):
    years = YearModel.objects.all().order_by(metric)
    serializer = YearSerializer(years, many=True)
    return Response(serializer.data)
