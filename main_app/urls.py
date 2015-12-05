from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^pollution$', views.PollutionForCoordinate.as_view()),
    url(r'^directions_for_workout$', views.DirectionsForWorkout.as_view()),
    url(r'^directions_A_to_B$', views.DirectionsAtoB.as_view()),
]
