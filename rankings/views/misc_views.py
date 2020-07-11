from rest_framework.decorators import api_view
from rest_framework.response import Response

import datetime
from rankings.event_pred import event_pred


@api_view(['GET'])
def EventPred(request):
    start = datetime.datetime.now()
    predictions = event_pred.quickSim(2019, "nccmp")
    end = datetime.datetime.now()
    print(end-start)
    return Response(predictions)
