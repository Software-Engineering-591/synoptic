from django.shortcuts import render  # noqa: F401
from django.views.generic import TemplateView
from manager.models import WaterReading
from sensor.models import Sensor
# Create your views here.


class HomeView(TemplateView):
    template_name = 'public/home.html'

    def get_context_data(self):
        return {
            's_and_wr': (
                (sensor, WaterReading.from_current(sensor))
                for sensor in Sensor.objects.all()
            )
        }
