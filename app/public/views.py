from django.shortcuts import render  # noqa: F401
from django.views.generic import TemplateView
from manager.models import WaterReading
from sensor.models import Sensor
from .weatherapi import get_weather_data, get_weekly_weather
from datetime import datetime
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


class WeatherView(TemplateView):
    template_name = 'public/weather.html'

    def get_context_data(self):
        import os

        lat = 12.629589810489191
        lon = 106.95043710454692
        appid = os.environ.get('WEATHERAPI_KEY')
        m = get_weather_data(lat=lat, lon=lon, appid=appid, units='metric')
        print(m.city)
        print(datetime.now().timestamp())
        if m.is_ok():
            return {'city': m.city, 'now': datetime.now().timestamp()}
        return {'city': None}


class PartialWeeklyWeatherView(TemplateView):
    template_name = 'partial/weather_weekly.html'

    def get_context_data(self):
        # Debugging rn so no return
        import os

        lat = 12.629589810489191
        lon = 106.95043710454692
        appid = os.environ.get('WEATHERAPI_KEY')
        m = get_weekly_weather(lat=lat, lon=lon, appid=appid, units='metric')
        if m is not None:
            return {'days': m}
        return {'days': None}


class PartialDailyWeatherView(TemplateView):
    template_name = 'partial/weather_daily.html'

    def get_context_data(self):
        # Debugging rn so no return
        import os

        lat = 12.629589810489191
        lon = 106.95043710454692
        appid = os.environ.get('WEATHERAPI_KEY')
        m = get_weather_data(lat=lat, lon=lon, appid=appid, units='metric')
        if m.is_ok():
            return {'weathers': m.list[:6]}
        return {'weathers': None}


class AlertView(TemplateView):
    template_name = 'public/alert.html'

    def get_context_data(self):
        return {'level': 'warning'}


class SettingsView(TemplateView):
    template_name = 'public/settings.html'
