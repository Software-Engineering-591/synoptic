from django.shortcuts import render  # noqa: F401
from django.views.generic import TemplateView
from manager.models import WaterReading
from sensor.models import Sensor
from .weatherapi import get_weather_data
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


class AlertView(TemplateView):
    template_name = 'public/alert.html'

    def get_context_data(self):
        # Debugging rn so no return
        import os

        lat = 12.629589810489191
        lon = 106.95043710454692

        appid = os.environ.get('WEATHERAPI_KEY')

        m = get_weather_data(lat=lat, lon=lon, appid=appid)
        if m.is_ok():
            return {'weathers': m.list[:4], 'city': m.city}
        print("Couldn't get weather data")
        return {'weathers': None, 'city': None}
