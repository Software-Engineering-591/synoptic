import json
from django.shortcuts import render, redirect  # noqa: F401
from django.contrib.auth import authenticate, login
from manager.forms import login_form, addSensorForm
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
    form = addSensorForm()
    points = Sensor.objects.values_list('point', flat=True)
    points_list = [{'lat': point.y, 'lon': point.x} for point in points]
    data = json.dumps(points_list, cls=DjangoJSONEncoder)
    fetched = request.GET.get('lat')
    return render(request, 'add_sensor.html', {'form' : form, 'data' : data, 'fetched' : fetched})
