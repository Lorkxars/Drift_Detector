from django.db import models
from drift_detector.models import DataSeries, DataPoint
import detection_algorithms.models as detection

import json
import socket
import sys
import pytz
from datetime import datetime
from django.db.models.signals import post_save

# Create your models here.
class Server(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=100)
    port = models.IntegerField()
    timestampLastUpdated = models.DateTimeField(blank=True, null=True)
    updateIntervalSeconds = models.IntegerField(default=300)

    dataSeries = models.OneToOneField(DataSeries, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



def save_profile(sender, **kwargs):
    if (kwargs['created']):
        print('signal recived')
        from .tasks import get_initial_data
        get_initial_data.delay(kwargs['instance'].id)

post_save.connect(save_profile, Server)


class Connection:
    server = None

    def __init__(self, server):
        self.server = server

    def get_first_data(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server.url, self.server.port))
            sock.send(("get_updates()" + '\r\n').encode())
            file = sock.recv(16384)
            sock.close()
            if(file != None):
                self.save_data(json.loads(file))
            else:
                print('No data available')

        except socket.gaierror:
            # this means could not resolve the host
            print("there was an error resolving the host")
            return None
        except socket.error as err:
            print("socket creation failed with error %s" % (err))
            return None
        except ValueError:
            print("no valid information returned from the host")
            return None

    def update_data(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((self.server.url, self.server.port))
            points = DataPoint.objects.filter(dataSeries=self.server.dataSeries)
            ts=[]
            for point in points:
                ts.append(point.timestampOriginal)
            timestamp = int(datetime.timestamp(max(ts)))
            sock.send(("get_updates(" + str(timestamp) + ")" + '\r\n').encode())
            file = sock.recv(16384)
            sock.close()
            if(file != None):
                self.save_data(json.loads(file))
            else:
                print('No data available')

        except socket.gaierror:
            # this means could not resolve the host
            print("there was an error resolving the host")
            return None
        except socket.error as err:
            print("socket creation failed with error %s" % (err))
            return None
        except ValueError:
            print("no valid information returned from the host")
            return None

    def update_status(dataSeries):
        points = DataPoint.objects.filter(dataSeries=dataSeries).exclude(timestampUpdated=None)
        print('points: ',len(points))
        if len(points) > 5:
            status = False
            for point in points[-5:]:
                status = status or point.cusum or point.ph or point.spc or point.sprt
            dataSeries.driftDetected=status
            print(status)
            dataSeries.save()

    def save_data(self, dataList):
        #iterate dataList
        for new_data_entry in dataList:
            original_timestamp  = datetime.utcfromtimestamp(int(new_data_entry.get('tsOriginal'))).replace(tzinfo=pytz.utc)
            x_axis = new_data_entry.get('xAxis')
            database_entry = DataPoint.objects.filter(timestampOriginal=original_timestamp, xAxis=x_axis)
            self.server.timestampLastUpdated = datetime.now()
            self.server.save()

            #Empty QuerySets are false:
            point = None
            if not database_entry:
                if(new_data_entry.get('tsUpdate')!= None):
                    updated_timestamp  = datetime.utcfromtimestamp(int(new_data_entry.get('tsUpdate'))).replace(tzinfo=pytz.utc)
                    point = DataPoint.create(timestampOriginal=original_timestamp, xAxis=new_data_entry.get('xAxis'), yAxisPredicted=new_data_entry.get('yAxisPredicted'), timestampUpdated=updated_timestamp, yAxisObserved=new_data_entry.get('yAxisObserved'), dataSeries=self.server.dataSeries)
                    point.absError = abs(point.yAxisPredicted - point.yAxisObserved)
                    point.cusum, point.ph, point.spc, point.sprt = detection.run_detection(point.absError,self.server.dataSeries)
                else:
                    point = DataPoint.create(timestampOriginal=original_timestamp, xAxis=new_data_entry.get('xAxis'), yAxisPredicted=new_data_entry.get('yAxisPredicted'), timestampUpdated=None, yAxisObserved=None, dataSeries=self.server.dataSeries)
                print(point)
                point.save()
            else:
                if(new_data_entry.get('tsUpdate')!= None):
                    entry = database_entry[0]
                    print(entry)
                    updated_timestamp  = datetime.utcfromtimestamp(int(new_data_entry.get('tsUpdate'))).replace(tzinfo=pytz.utc)
                    entry.timestampUpdated = updated_timestamp
                    entry.yAxisObserved = new_data_entry.get('yAxisObserved')
                    entry.absError = abs(entry.yAxisPredicted - entry.yAxisObserved)
                    entry.cusum, entry.ph, entry.spc, entry.sprt = detection.run_detection(entry.absError,self.server.dataSeries)
                    entry.save()
        self.update_status(self.server.dataSeries)
