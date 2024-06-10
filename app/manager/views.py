from django.shortcuts import render, redirect  # noqa: F401
from .models import WaterReading
import io
import base64
import matplotlib.pyplot as plt
from sensor.models import Sensor
import json
from django.utils.translation import gettext as _

# Create your views here.


# graph
def generate_graph(readings, parameter, title, ylabel):
    plt.figure(figsize=(6, 4))
    timestamps = [reading.timestamp for reading in readings]
    values = [getattr(reading, parameter) for reading in readings]
    plt.plot(timestamps, values, marker='o')
    plt.xlabel(_('Timestamp'))
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=45)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.1)
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()

    graph = base64.b64encode(image_png).decode('utf-8')
    return graph


def dashboard(request):
    readings = WaterReading.objects.select_related('sensor').order_by('timestamp')

    sensors = Sensor.objects.all()
    geo_data = [
        {
            'id': sensor.id,
            'name': sensor.name,
            'point': (
                sensor.point.y,
                sensor.point.x,
            ),  # lat is y and long is x
        }
        for sensor in sensors
    ]

    # matplotlib data
    readings_data = [
        {
            'id': reading.id,
            'level': reading.level,
            'orp': reading.orp,
            'ph': reading.ph,
            'bod': reading.bod,
            'temperature': reading.temperature,
            'timestamp': reading.timestamp.strftime('%m-%d %H:%M'),
        }
        for reading in readings
    ]

    # For each sensor,
    sensors_data = []
    for sensor in sensors:
        readings = WaterReading.objects.filter(sensor=sensor).order_by('timestamp')

        if readings.exists():
            sensor_temperature = generate_graph(
                readings,
                'temperature',
                _('Temperature for {sensor_name}').format(sensor_name=sensor.name),
                _('Temperature (°C)'),
            )

            sensor_level = generate_graph(
                readings, 'level', _('Water Level for {sensor_name}').format(sensor_name=sensor.name), _('Level (m)')
            )

            sensor_orp = generate_graph(
                readings, 'orp', _('ORP for {sensor_name}').format(sensor_name=sensor.name), _('ORP (mV)')
            )

            sensor_ph = generate_graph(readings, 'ph', _('pH for {sensor_name}').format(sensor_name=sensor.name), _('pH'))

            sensor_bod = generate_graph(readings, 'bod', _('BOD for {sensor_name}').format(sensor_name=sensor.name), _('BOD'))

            sensors_data.append({
                'sensor': sensor,
                'level_graph': sensor_level,
                'orp_graph': sensor_orp,
                'ph_graph': sensor_ph,
                'bod_graph': sensor_bod,
                'temperature_graph': sensor_temperature,
                'latest': readings.last(),
            })

        # if readings.exists():
        #     sensor_temperature = generate_graph(
        #         readings,
        #         'temperature',
        #         _('Temperature for %(name)s') % {'name': sensor.name},
        #         _('Temperature (°C)'),
        #     )

        #     sensor_level = generate_graph(
        #         readings, 'level', f'Water Level for {sensor.name}', 'Level (m)'
        #     )

        #     sensor_orp = generate_graph(
        #         readings, 'orp', f'ORP for {sensor.name}', 'ORP (mV)'
        #     )

        #     sensor_ph = generate_graph(readings, 'ph', f'pH for {sensor.name}', 'pH')

        #     sensor_bod = generate_graph(
        #         readings, 'bod', f'BOD for {sensor.name}', 'BOD'
        #     )
        #     sensors_data.append(
        #         {
        #             'sensor': sensor,
        #             'level_graph': sensor_level,
        #             'orp_graph': sensor_orp,
        #             'ph_graph': sensor_ph,
        #             'bod_graph': sensor_bod,
        #             'temperature_graph': sensor_temperature,
        #             'latest': readings.last(),
        #         }
        #     )

    return render(
        request,
        'manager/dashboard.html',
        {
            'readings': readings,
            'sensors': sensors_data,
            'geo_data': json.dumps(geo_data),
            'readings_data': readings_data,
        },
    )
