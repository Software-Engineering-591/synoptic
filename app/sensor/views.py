from django.shortcuts import render  # noqa: F401
from .models import Sensor

# Create your views here.
def home(request):
    sensors = Sensor.objects.all()
    return render(request, 'home.html', {'sensors': sensors})