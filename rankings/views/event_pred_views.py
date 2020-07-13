from rest_framework.decorators import api_view
from rest_framework.response import Response

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rankings.event_pred import event_pred


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("")},
    operation_description="Returns predicted RP and Tiebreaker Score for all" +
                          " teams, using data from an inputted index",
)
@api_view(['GET'])
def MeanSim(request, event, index):
    year, event = int(event[:4]), event[4:]
    predictions = event_pred.meanSim(year, event, int(index))
    return Response(predictions)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("")},
    operation_description="Returns predicted RP, predicted Rank," +
                          " Rank Probabilities, and Tiebreaker Score for all" +
                          " teams, using data from an inputted index",
)
@api_view(['GET'])
def IndexSim(request, event, index, iterations=100):
    year, event = int(event[:4]), event[4:]
    predictions = event_pred.indexSim(year, event, int(index), int(iterations))
    return Response(predictions)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("")},
    operation_description="Returns predicted RP and Tiebreaker Score for all" +
                          " teams, using data from the end of each match",
)
@api_view(['GET'])
def QuickSim(request, event):
    year, event = int(event[:4]), event[4:]
    predictions = event_pred.quickSim(year, event)
    return Response(predictions)


@swagger_auto_schema(
    method='GET', responses={200: openapi.Response("")},
    operation_description="Returns predicted RP, predicted Rank," +
                          " Rank Probabilities, and Tiebreaker Score for all" +
                          " teams, simulated from the end of each match",
)
@api_view(['GET'])
def Sim(request, event, iterations=100):
    year, event = int(event[:4]), event[4:]
    predictions = event_pred.sim(year, event, int(iterations))
    return Response(predictions)
