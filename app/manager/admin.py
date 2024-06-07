from django.contrib import admin  # noqa: F401
from .models import Sensor, WaterReading

# Register your models here.
admin.site.register([Sensor, WaterReading])