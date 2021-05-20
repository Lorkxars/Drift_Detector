from rest_framework import serializers
from drift_detector.models import DataSeries, DataPoint


class DataSeriesSerializer(serializers.ModelSerializer):
    data_points = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    class Meta:
        model = DataSeries
        fields = '__all__'



class DataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataPoint
        fields = '__all__'
