from rest_framework import status  # Import this for Status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response  # Import this for Response
from rest_framework.viewsets import GenericViewSet

from drift_detector.models import DataSeries, DataPoint
from drift_detector_api.serializers import DataSeriesSerializer, DataPointSerializer
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.views import APIView

class DataSeriesViewSet(generics.ListCreateAPIView):
    queryset = DataSeries.objects.all()
    serializer_class = DataSeriesSerializer


class DataSeriesDetail(APIView):
    def get(self, request, prim):
        queryset = DataSeries.objects.get(pk=prim)
        print(queryset)
        data = DataSeriesSerializer(queryset).data
        return Response(data, status=status.HTTP_200_OK)

class DataPointList(generics.ListCreateAPIView):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer


class DataPointDetail(generics.RetrieveDestroyAPIView):
    queryset = DataPoint.objects.all()
    serializer_class = DataPointSerializer

class DataSeriesPointsTimestamp(APIView):
    def get(self, request, prim, timestamp):
        queryset = DataSeries.objects.get(pk=prim)
        data = DataSeriesSerializer(queryset).data
        list = []
        # Filter for updated points newer than the given timestamp
        for point in data["data_points"]:
            candidate = DataPoint.objects.get(pk=point)
            if(candidate.timestampUpdated != None):
                if(candidate.timestampUpdated.timestamp() > timestamp):
                    list.append(candidate)

        data = DataPointSerializer(list, many=True).data
        return Response(data, status=status.HTTP_200_OK)
