from django.db import models
from sensor.models import Sensor
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class WaterReading(models.Model):
    """
    WaterReading model
    """

    level = models.FloatField()
    orp = models.FloatField()  # oxidation reduction potential
    ph = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(14)],
    )
    bod = models.FloatField(
        validators=[MinValueValidator(0)]
    )  # biological oxygen demand
    temperature = models.FloatField()  # Celsius
    timestamp = models.DateTimeField(auto_now_add=True)

    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE)

    def __str__(self):
        return f'WaterReading {self.id} - {self.sensor}'

    def clean_condition(self):
        """
        Check if the water reading is in clean condition

        Clean Condition:
        ORP should be between +200 to +500 mV
        pH should be between 6.5 to 8.5
        bod should be between 1-2 mg/L
        """
        return (
            (200 <= self.orp <= 500)
            and (6.5 <= self.ph <= 8.5)
            and (1 <= self.bod <= 2)
        )

    @staticmethod
    def from_current(sensor: Sensor):
        """
        Get latest reading from sensor

        Can return None in the case that it hasn't made a reading.
        """
        return WaterReading.objects.filter(sensor=sensor).order_by('-timestamp').first()
