from django.shortcuts import render, redirect  # noqa: F401
from django.views.generic import TemplateView
from django.contrib.auth import authenticate, login
from manager.forms import login_form, addSensorForm
from django.core.exceptions import ValidationError
from django.http import JsonResponse
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
     form = addSensorForm()
     return render(request, 'add_sensor.html', {'form' : form})

def selected_location(request):
    latitude = request.GET.get('latitude')
    longitude = request.GET.get('longitude')
    print(latitude, longitude)

    a = Sensor.objects.create(
         point = Point(float(longitude), float(latitude)), 
         name='Sensor 1'
         )
    a.save()
         
    return JsonResponse({})

    