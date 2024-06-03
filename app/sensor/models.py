from django.db import models  # noqa: F401
from django.contrib.gis.db import models as geomodels
import uuid
# Create your models here.


class Sensor(models.Model):
    point = geomodels.PointField()
    name = models.CharField(max_length=255)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return self.main_carstring
