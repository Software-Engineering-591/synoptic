import json
from django.utils import timezone
from django.shortcuts import render, redirect  # noqa: F401
from django.contrib.auth import authenticate, login
from manager.forms import login_form, addSensorForm, latandlon
from django.core.serializers.json import DjangoJSONEncoder
from .models import WaterReading, Sensor
from django.contrib.gis.geos import Point

# Create your views here.
def adminView(request):
    if request.method == 'POST':
        attempt = login_form(request, data=request.POST)
        if attempt.is_valid():
            username1 = attempt.cleaned_data['username']
            password1 = attempt.cleaned_data['password']
            user = authenticate(request, username=username1, password=password1)

            if user is not None:
                    login(request, user)
                    return render(request, 'add_sensor.html')
            else:
                return render(request, 'admin_login.html', {'form' : attempt})
        else:
            return render(request, 'admin_login.html', {'form' : attempt})
    else:
        attempt = login_form()
        return render(request, 'admin_login.html', {'form' : attempt})
    

def mapView(request):
    if not request.user.is_authenticated:
         return redirect('login')
    points = Sensor.objects.values_list('point', flat=True)
    points_list = [{'lat': point.y, 'lon': point.x} for point in points]
    data = json.dumps(points_list, cls=DjangoJSONEncoder)
    fetched_lat = request.GET.get('lat') or request.POST.get('lat')
    fetched_lon = request.GET.get('longitude') 
    print(fetched_lat)
    form = addSensorForm()
    latform = latandlon()
    if request.method == 'POST':
        form = addSensorForm(request.POST)
        latform = latandlon(request.POST)
            
        fetched_lat = request.POST.get('lat')
        fetched_lon = request.GET.get('longitude')
        print(fetched_lat)
        if fetched_lat and fetched_lon:
            print(f'Form data: {request.POST}')
           
            if form.is_valid():     
            
                Waterreading = WaterReading.objects.create(
                    level = form.cleaned_data['level'],
                    orp = form.cleaned_data['orp'],
                    bod = form.cleaned_data['ph'],
                    temperature = form.cleaned_data['temperature'],
                    sensor = Sensor.objects.get(point=Point(float(fetched_lon), float(fetched_lat))),
                    timestamp = timezone.now()
                )
                Waterreading.save()
                return render(request, 'add_sensor.html', {'form' : form, 'data' : data})
            else:
                form = addSensorForm()
                latform = latandlon()
                return render(request, 'add_sensor.html', {'form' : form, 'data' : data, 'lat_form' : latform})
        else:
            return render(request, 'add_sensor.html', {'form' : form, 'data' : data, 'lat_form' : latform})
    else:
        return render(request, 'add_sensor.html', {'form' : form, 'data' : data, 'lat_form' : latform})

