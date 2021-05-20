from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('drift_detector.urls', namespace='drift_detector')),
    path('api/', include('drift_detector_api.urls', namespace='drift_detector_api')),
]
