from django.contrib import admin  # noqa: F401
from .models import Sensor
from leaflet.admin import LeafletGeoAdmin
# Register your models here.

admin.site.register(Sensor, LeafletGeoAdmin)
