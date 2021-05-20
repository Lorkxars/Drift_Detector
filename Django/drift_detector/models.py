from django.db import models

class DataSeries(models.Model):
    name = models.CharField(max_length=200)
    thumbnail = models.ImageField(blank=True, upload_to='static/images')
    driftDetected = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = "Data series"

class DataPoint(models.Model):
    #Data on when first created
    timestampOriginal = models.DateTimeField()
    xAxis = models.FloatField()
    yAxisPredicted = models.FloatField()

    #Data arriving on server update
    timestampUpdated = models.DateTimeField(blank=True, null=True)
    yAxisObserved = models.FloatField(blank=True, null=True)

    #Data to be recovered from drift module with server updated new data
    absError = models.FloatField(blank=True, null=True)
    cusum = models.BooleanField(blank=True, null=True)
    ph = models.BooleanField(blank=True, null=True)
    spc = models.BooleanField(blank=True, null=True)
    sprt = models.BooleanField(blank=True, null=True)

    dataSeries = models.ForeignKey(DataSeries, on_delete=models.CASCADE, related_name='data_points')

    def __str__(self):
        return "(" + str(self.xAxis) +  ", " + str(self.yAxisPredicted) +")"

    @classmethod
    def create(cls, timestampOriginal, xAxis, yAxisPredicted,timestampUpdated,yAxisObserved,dataSeries):
        point = cls(timestampOriginal=timestampOriginal, xAxis=xAxis, yAxisPredicted=yAxisPredicted, timestampUpdated=timestampUpdated, yAxisObserved=yAxisObserved, dataSeries=dataSeries)
        return point
