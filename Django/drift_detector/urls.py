from django.urls import path
from django.views.generic import TemplateView

app_name = 'drift_detector'

urlpatterns = [
     path('', TemplateView.as_view(template_name="drift_detector/index.html")),


]

