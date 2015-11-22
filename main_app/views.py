from django.shortcuts import render
from rest_framework.views import APIView, Response
from utils import getPolutionPoints

# Create your views here.


class PolutionDataForBoundedBoxView(APIView):
    permission_classes = []

    def get(self, request):
        pointsJSON = getPolutionPoints(request.GET['LTx'],request.GET['LTy'],request.GET['RBx'],request.GET['RBw'])
        try:
            return Response(pointsJSON)
        except Exception as e:
            import traceback
            print traceback.format_exc()
