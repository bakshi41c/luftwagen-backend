from django.shortcuts import render
from rest_framework.views import APIView, Response
from utils.pollution_directions import getRandomDirections, getRandomDirectionsAtoB, \
    addPollutionLeveltoRoutes, bestThreeRoutes
import utils.pollution as pollution

# Create your views here.


class PollutionForCoordinate(APIView):
    permission_classes = []

    def get(self, request):
        pollution_value = pollution.get_pollution_value(float(request.GET['lat']), float(request.GET['long']), 0)
        json_response = {"pollution" : pollution_value}
        try:
            return Response(json_response)
        except Exception:
            import traceback
            print traceback.format_exc()


class DirectionsForWorkout(APIView):
    permission_classes = []

    def get(self, request):
        directions = getRandomDirections(float(request.GET['lat']), float(request.GET['long']),
                                         float(request.GET['distance']))
        addPollutionLeveltoRoutes(directions)
        try:
            return Response(bestThreeRoutes(directions))
        except Exception:
            import traceback
            print traceback.format_exc()


class DirectionsAtoB(APIView):
    permission_classes = []

    def get(self, request):
        directions = getRandomDirectionsAtoB(float(request.GET['Alat']), float(request.GET['Along']),
                                             float(request.GET['Blat']), float(request.GET['Blong']))
        addPollutionLeveltoRoutes(directions)
        try:
            return Response(bestThreeRoutes(directions))
        except Exception:
            import traceback
            print traceback.format_exc()
