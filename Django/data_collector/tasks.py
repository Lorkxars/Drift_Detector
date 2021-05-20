from __future__ import absolute_import, unicode_literals
from .models import Server, Connection
from datetime import datetime
from django.utils.timezone import utc

from celery import shared_task
from celery.decorators import task

@shared_task
def add(x, y):
    return x + y

@task(name="get_initial_data")
def get_initial_data(server_id):
    Connection(Server.objects.get(id=server_id)).get_first_data()

@task(name="update_server_data")
def update_server_data(server_id):
    Connection(Server.objects.get(id=server_id)).update_data()

@task(name="get_initial_server_data")
def get_initial_server_data(server_id):
    Connection(Server.objects.get(id=server_id)).get_first_data()

@shared_task
def cycle_servers():
    for server in Server.objects.all():
        if(server.timestampLastUpdated != None):
            if((datetime.now().replace(tzinfo=utc) - server.timestampLastUpdated).seconds > server.updateIntervalSeconds):
                print('updating: ' + server.name)
                update_server_data.delay(server.id)
        else:
            print('Trying to get initial data of: ' + server.name)
            get_initial_server_data.delay(server.id)
