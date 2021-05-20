from django.contrib import admin

# Register your models here.
from drift_detector.models import DataSeries, DataPoint
from data_collector.models import Server
from detection_algorithms.models import Cusum, PageHinkleyClass, SPC, SPRT

admin.site.register(DataSeries)
admin.site.register(DataPoint)
admin.site.register(Server)
class CusumAdmin(admin.ModelAdmin):
    exclude = ('accumulator',)
admin.site.register(Cusum, CusumAdmin)
class PHAdmin(admin.ModelAdmin):
    exclude = ('x_mean','sample_count','sum','in_concept_change',)
admin.site.register(PageHinkleyClass, PHAdmin)
admin.site.register(SPC)
admin.site.register(SPRT)
