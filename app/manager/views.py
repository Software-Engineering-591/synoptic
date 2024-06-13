import base64
import io
import json

import matplotlib.pyplot as plt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.gis.geos import Point
from django.shortcuts import redirect, render, reverse, get_object_or_404
from django.utils import timezone
from django.utils.translation import gettext as _
from django_htmx.http import HttpResponseClientRedirect
from django.views.generic import TemplateView


from manager.forms import AddSensorForm, Addwaterform, Latandlon, LoginForm

from .models import Sensor, WaterReading

# Create your views here.


# graph
def generate_graph(readings, parameter, title, ylabel, **kwargs):
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



class AlertGraphView(TemplateView):
    template_name = 'partial/manager_graph.html'

    def get_context_data(self, **kwargs):
        s = super().get_context_data(**kwargs)
        id = self.request.GET.get('sensor_id') or 0
        sensor = get_object_or_404(Sensor, id=id)
        try:
            id = int(id)
        except:
            return {"graph": ""}
        readings = WaterReading.objects.filter(sensor=sensor).order_by('timestamp')
        param = self.request.GET.get('param') or ""
        print(id, param)
        print (self.kwargs)
        title = {
            'level': _('Water Level'),
            'orp': _('ORP'),
            'ph': _('pH'),
            'bod': _('BOD'),
            'temperature': _('Temperature'),
        }
        ylabel = {
            'level': _('m'),
            'orp': _('mV'),
            'ph': _('pH'),
            'bod': _('BOD'),
            'temperature': _('°C'),
        }
        graph = generate_graph(readings, param, title.get(param, None), ylabel.get(param, None))
        return {"graph": graph}

def manager_graph(request, sensor_id, param):

    sensor = get_object_or_404(Sensor, id=sensor_id)
    readings = WaterReading.objects.filter(sensor=sensor).order_by('timestamp')
    title = {
        'level': _('Water Level'),
        'orp': _('ORP'),
        'ph': _('pH'),
        'bod': _('BOD'),
        'temperature': _('Temperature'),
    }
    ylabel = {
        'level': _('m'),
        'orp': _('mV'),
        'ph': _('pH'),
        'bod': _('BOD'),
        'temperature': _('°C'),
    }
    print(sensor)
    print(readings)
    print(f"{param=}")
    return render(request, 'partial/manager_graph.html', {'graph': generate_graph(readings, param, title.get(param, None), ylabel.get(param, None)),})


@login_required(login_url='login')
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


def login_view(request):
    """
    This view handles a login request by the user.
    """
    form = (
        LoginForm(request, data=request.POST)
        if request.method == 'POST'
        else LoginForm()
    )
    # If the form is valid
    if form.is_valid():
        # Authenticating user
        user = authenticate(
            request,
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password'],
        )

        if user is not None:
            # If the user exists, login the user
            login(request, user)
            return redirect('dashboard')

    return render(request, 'manager/admin_login.html', {'form': form})


@login_required(login_url='login')
def add_water_view(request):
    """
    This view handles creating a new water reading object at the request of the user
    """

    form = Addwaterform()
    latform = Latandlon()
    # grabbing all of the points into a list and then converting points to json
    sensors = Sensor.objects.all()
    # Getting point attributes from a list of points from sensor objects
    sensor_info = [
        {'lat': sensor.point.y, 'lon': sensor.point.x, 'name': sensor.name}
        for sensor in sensors
    ]
    # dumping json converted data
    data = json.dumps(sensor_info)

    ## If the user submits
    if request.method == 'POST':
        ## post forms
        form = Addwaterform(request.POST)
        latform = Latandlon(request.POST)

        if form.is_valid() and latform.is_valid():
            ## Grabbing the latandlon form data to filter sensor later
            fetched_lat = latform.cleaned_data['lat']
            fetched_lon = latform.cleaned_data['lon']

            ## Creating new water reading object
            water_reading = WaterReading.objects.create(
                level=form.cleaned_data['level'],
                orp=form.cleaned_data['orp'],
                bod=form.cleaned_data['bod'],
                ph=form.cleaned_data['ph'],
                temperature=form.cleaned_data['temperature'],
                # Filtering the point value
                sensor=Sensor.objects.get(point=Point(fetched_lon, fetched_lat)),
                timestamp=timezone.now(),
            )
            ## Saving the new object
            water_reading.save()
            return redirect('dashboard')
        else:
            form = Addwaterform()
            latform = Latandlon()
            return render(
                request,
                'manager/add_water_reading.html',
                {'form': form, 'data': data, 'lat_form': latform},
            )
    else:
        return render(
            request,
            'manager/add_water_reading.html',
            {'form': form, 'data': data, 'lat_form': latform},
        )


def add_sensor_view(request):
    """
    This view will handle creating a new sensor object at the request of the user.
    """
    latform = Latandlon()
    sensorform = AddSensorForm()

    if request.method == 'POST':
        sensorform = AddSensorForm(request.POST)
        latform = Latandlon(request.POST)
        # If the forms are valid
        if sensorform.is_valid() and latform.is_valid():
            latitude = latform.cleaned_data['lat']
            longitude = latform.cleaned_data['lon']
            # Creating new sensor object
            new_sensor = Sensor.objects.create(
                name=sensorform.cleaned_data['name'],
                # Creating new point object and assigning it to new object point
                point=Point(float(longitude), float(latitude)),
            )
            new_sensor.save()
            return redirect('dashboard')
        else:
            return render(
                request,
                'manager/add_sensor.html',
                {'latform': latform, 'sensorform': sensorform},
            )
    else:
        return render(
            request,
            'manager/add_sensor.html',
            {'latform': latform, 'sensorform': sensorform},
        )


@require_POST
def logout_view(request):
    """
    Handles logout request by user.
    """
    logout(request)
    if request.htmx:
        return HttpResponseClientRedirect(reverse('login'))
    return redirect('login')
