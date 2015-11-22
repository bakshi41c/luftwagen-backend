from django.shortcuts import render
from rest_framework.views import APIView, Response
from utils import getPolutionPoints

# Create your views here.


class PolutionDataForBoundedBoxView(APIView):
    permission_classes = []

    def get(self, request):
        pointsJSON = getPolutionPoints(request.GET['x'],request.GET['y'],request.GET['length'],request.GET['width'])
        try:
            return Response(pointsJSON)
        except Exception as e:
            import traceback
            print traceback.format_exc()
