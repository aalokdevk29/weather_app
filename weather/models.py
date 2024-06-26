from django.db import models
from django.utils import timezone


class WeatherData(models.Model):
    latitude: float = models.FloatField()
    longitude: float = models.FloatField()
    detailing_type: str = models.CharField(max_length=50)
    data: dict = models.JSONField()
    timestamp: timezone.datetime = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("latitude", "longitude", "detailing_type")

    def __str__(self):
        return f"Weather data for ({self.latitude}, {self.longitude}) [{self.detailing_type}]"
