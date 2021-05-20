from django.contrib import admin
from django.urls import path

from drift_detector_api import views


app_name = 'drift_detector_api'

urlpatterns = [
    path('', views.DataSeriesViewSet.as_view(), name='data_sries_view_set'),
    path('<int:prim>/', views.DataSeriesDetail.as_view(), name="data_series_detail"),

    path('datapoints/', views.DataPointList.as_view(), name='data_point_list'),
    path('datapoints/<int:pk>/', views.DataPointDetail.as_view(), name="data_point_detail"),

    path('<int:prim>/<int:timestamp>', views.DataSeriesPointsTimestamp.as_view(), name="data_series_points_timestamp"),
]
