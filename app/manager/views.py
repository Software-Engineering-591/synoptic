import json
from django.utils import timezone
from django.shortcuts import render, redirect  # noqa: F401
import io
import base64
import matplotlib.pyplot as plt
from django.utils.translation import gettext as _
from django.contrib.auth import authenticate, login
from manager.forms import Loginform, Addensorform, Latandlon
from django.core.serializers.json import DjangoJSONEncoder
from .models import WaterReading, Sensor
from django.contrib.gis.geos import Point

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
                readings,
                'level',
                _('Water Level for {sensor_name}').format(sensor_name=sensor.name),
                _('Level (m)'),
            )

            sensor_orp = generate_graph(
                readings,
                'orp',
                _('ORP for {sensor_name}').format(sensor_name=sensor.name),
                _('ORP (mV)'),
            )

            sensor_ph = generate_graph(
                readings,
                'ph',
                _('pH for {sensor_name}').format(sensor_name=sensor.name),
                _('pH'),
            )

            sensor_bod = generate_graph(
                readings,
                'bod',
                _('BOD for {sensor_name}').format(sensor_name=sensor.name),
                _('BOD'),
            )

            sensors_data.append(
                {
                    'sensor': sensor,
                    'level_graph': sensor_level,
                    'orp_graph': sensor_orp,
                    'ph_graph': sensor_ph,
                    'bod_graph': sensor_bod,
                    'temperature_graph': sensor_temperature,
                    'latest': readings.last(),
                }
            )

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

def admin_view(request):
    if request.method == 'POST':
        attempt = Loginform(request, data=request.POST)
        if attempt.is_valid():
            username1 = attempt.cleaned_data['username']
            password1 = attempt.cleaned_data['password']
            user = authenticate(request, username=username1, password=password1)

            if user is not None:
                    login(request, user)
                    ## This should be changed to admin dashboard
                    return redirect('dashboard')
            else:
                return render(request, 'manager/admin_login.html', {'form' : attempt})
        else:
            return render(request, 'manager/admin_login.html', {'form' : attempt})
    else:
        attempt = Loginform()
        return render(request, 'manager/admin_login.html', {'form' : attempt})
    

def add_sensor_view(request):
    if not request.user.is_authenticated:
         return redirect('login')
    form = Addensorform()
    latform = Latandlon()
    ## grabbing all of the points into a list and then converting points to json
    points = Sensor.objects.values_list('point', flat=True)
    ## Getting point attributes from a list of points from sensor objects
    points_list = [{'lat': point.y, 'lon': point.x} for point in points]
    ## dumping json converted data
    data = json.dumps(points_list, cls=DjangoJSONEncoder)
    
    fetched_lat = request.GET.get('lat')
    fetched_lon = request.GET.get('longitude')
    ## If the user submits
    if request.method == 'POST':
        ## post forms
        form = Addensorform(request.POST)
        latform = Latandlon(request.POST)
        if form.is_valid() and latform.is_valid():  
            ## Grabbing the latandlon form data to filter sensor later   
            fetched_lat = latform.cleaned_data['lat']
            fetched_lon = latform.cleaned_data['lon']
           
            ## Creating new water reading object
            water_reading = WaterReading.objects.create(
                level = form.cleaned_data['level'],
                orp = form.cleaned_data['orp'],
                bod = form.cleaned_data['bod'],
                ph = form.cleaned_data['ph'],
                temperature = form.cleaned_data['temperature'],
                sensor = Sensor.objects.get(point=Point(fetched_lon, fetched_lat)),
                timestamp = timezone.now()
            )
            ## Saving the new object
            water_reading.save()
            return redirect('dashboard')
        else:
            form = Addensorform()
            latform = Latandlon()
            return render(request, 'manager/add_sensor.html', {'form' : form,
                                                                'data' : data,
                                                        'lat_form' : latform})
    else:
        return render(request, 'manager/add_sensor.html', {'form' : form, 'data' : data,
                                                    'lat_form' : latform})


