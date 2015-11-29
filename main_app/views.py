from django.shortcuts import render
from rest_framework.views import APIView, Response
from utils import getPolutionPoints, getRandomDirections, getRandomDirectionsAtoB

# Create your views here.


class PolutionDataForBoundedBoxView(APIView):
    permission_classes = []

    def get(self, request):
        pointsJSON = getPolutionPoints(float(request.GET['LTx']),float(request.GET['LTy']),
                                       float(request.GET['RBx']),float(request.GET['RBw']))
        try:
            return Response(pointsJSON)
        except Exception:
            import traceback
            print traceback.format_exc()


class DirectionsForWorkout(APIView):
    permission_classes = []

    def get(self, request):
        directions = getRandomDirections(float(request.GET['lat']),float(request.GET['long']),float(request.GET['distance']))
        try:
            return Response(directions)
        except Exception:
            import traceback
            print traceback.format_exc()

class DirectionsAtoB(APIView):
    permission_classes = []

    def get(self, request):
        directions = getRandomDirectionsAtoB(float(request.GET['Alat']),float(request.GET['Along']),
                                             float(request.GET['Blat']),float(request.GET['Blong']))
        try:
            return Response(directions)
        except Exception:
            import traceback
            print traceback.format_exc()

