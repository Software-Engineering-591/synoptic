from django.shortcuts import render, get_object_or_404  # noqa: F401
import base64
from enum import Enum
from django.views.generic import TemplateView
from manager.models import WaterReading
from sensor.models import Sensor
from .weatherapi import get_weather_data, get_weekly_weather
from datetime import datetime
from matplotlib import pyplot as plt
from django.conf import settings
import io
import json
from django.utils.translation import gettext as _
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
        m = get_weather_data(**settings.WEATHER_INFO, units='metric')
        print(m.city)
        print(datetime.now().timestamp())
        if m.is_ok():
            return {'city': m.city, 'now': datetime.now().timestamp()}
        return {'city': None}


class PartialWeeklyWeatherView(TemplateView):
    template_name = 'partial/weather_weekly.html'

    def get_context_data(self):
        m = get_weekly_weather(**settings.WEATHER_INFO, units='metric')
        if m is not None:
            return {'days': m}
        return {'days': None}


class PartialDailyWeatherView(TemplateView):
    template_name = 'partial/weather_daily.html'

    def get_context_data(self):
        m = get_weather_data(**settings.WEATHER_INFO, units='metric')
        if m.is_ok():
            return {'weathers': m.list[:6]}
        return {'weathers': None}


DANGER_LEVEL = 5  # M
WARNING_LEVEL = 2.5  # M


class AlertLevel(Enum):
    SUCCESS = 0
    WARNING = 1
    ERROR = 2


class EnhancedJsonEncoder(json.JSONEncoder):
    def default(self, o):
        # if instance of AlertLevel, return the name of the enum
        if isinstance(o, AlertLevel):
            return o.name.lower()
        return super().default(o)


class AlertView(TemplateView):
    template_name = 'public/alert.html'

    def get_context_data(self):
        daily_weathers = get_weekly_weather(**settings.WEATHER_INFO, units='metric')
        if daily_weathers is None:
            return {'level': 'success'}

        # Need to caclulate if the sensor is at risk of flood
        sensors = Sensor.objects.all()

        sensors_data = []
        for sensor in sensors:
            readings = WaterReading.objects.filter(sensor=sensor).order_by(
                '-timestamp'
            )[:2]
            if readings.exists():
                if readings[0].level > DANGER_LEVEL:
                    level = AlertLevel.ERROR
                elif readings[0].level > WARNING_LEVEL:
                    level = AlertLevel.WARNING
                else:
                    level = AlertLevel.SUCCESS
                sensors_data.append(
                    {
                        'sensor': {
                            'id': sensor.id,
                            'name': sensor.name,
                            'point': sensor.point.coords[
                                ::-1
                            ],  # reverse the order since the coords is [lat, lng]
                        },
                        'level': level,
                    }
                )

        return {
            'level': max(
                sensors_data,
                key=lambda x: x['level'].value,
            )['level'].name.lower()
            if sensors_data
            else 'success',
            'sensors': json.dumps(sensors_data, cls=EnhancedJsonEncoder),
        }


def alert_graph(sensor, reading):
    plt.figure(figsize=(6, 4))

    daily_weathers = get_weekly_weather(**settings.WEATHER_INFO, units='metric')
    if daily_weathers is None:
        return None

    rainfalls = [weather.total_rain for weather in daily_weathers]
    days = [weather.date.day for weather in daily_weathers]

    plt.plot(days, rainfalls, marker='o')
    plt.xlabel(_('Current Day'))
    plt.ylabel(_('Rainfall(mm)'))
    plt.xticks(days)
    plt.axhline(y=max(WARNING_LEVEL - reading.level, 0) * 100, color='orange')
    plt.axhline(y=max(DANGER_LEVEL - reading.level, 0) * 100, color='red')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode('utf-8')

    return graph


class AlertGraphView(TemplateView):
    template_name = 'partial/alert_graph.html'

    def get_context_data(self, **kwargs):
        id = self.request.GET.get('sensor_id')
        sensor = get_object_or_404(Sensor, id=id)
        reading = WaterReading.objects.filter(sensor=sensor).latest('-timestamp')
        graph = alert_graph(sensor, reading)
        return {
            'graph': graph,
            'sensor': sensor,
            'reading': reading,
        }


class SettingsView(TemplateView):
    template_name = 'public/settings.html'


class GoalsView(TemplateView):
    template_name = 'public/our-goals.html'
