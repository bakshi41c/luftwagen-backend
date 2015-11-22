from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get_pollution_data_for_bounded_box$', views.PolutionDataForBoundedBoxView.as_view(), name='getPolutionDataForBoundedBoxView'),
]