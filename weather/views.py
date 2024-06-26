import logging
from datetime import timedelta

import requests
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.conf import settings
from .models import WeatherData
from .serializers import WeatherDataSerializer

logger = logging.getLogger(__name__)


class WeatherAPIView(APIView):
    def get(self, request, format=None) -> Response:
        lat = request.query_params.get("lat")
        lon = request.query_params.get("lon")
        detailing_type = request.query_params.get("detailing_type")

        if not lat or not lon or not detailing_type:
            return Response(
                {"error": "lat, lon and detailing_type are required parameters"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            return Response(
                {"error": "lat and lon must be valid float numbers"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        detailing_types = ["current", "minutely", "hourly", "daily"]
        if detailing_type not in detailing_types:
            return Response(
                {"error": f"detailing_type must be one of {detailing_types}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        weather_data = WeatherData.objects.filter(
            latitude=lat, longitude=lon, detailing_type=detailing_type
        ).first()

        if weather_data and timezone.now() - weather_data.timestamp < timedelta(
            minutes=settings.CACHE_DURATION
        ):
            serializer = WeatherDataSerializer(weather_data)
            return Response(serializer.data)

        data = self.fetch_weather_data(lat, lon, detailing_type)
        if data is None:
            return Response(
                {"error": "Failed to fetch data from OpenWeatherMap"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if weather_data:
            weather_data.data = data
            weather_data.timestamp = timezone.now()
            weather_data.save()
        else:
            weather_data = WeatherData.objects.create(
                latitude=lat, longitude=lon, detailing_type=detailing_type, data=data
            )

        serializer = WeatherDataSerializer(weather_data)
        return Response(serializer.data)

    def fetch_weather_data(self, lat: float, lon: float, detailing_type: str) -> dict:
        print(settings.OPENWEATHERMAP_API_KEY)
        """Fetch weather data from OpenWeatherMap API."""
        url = f"http://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&exclude=&appid={settings.OPENWEATHERMAP_API_KEY}"
        exclude = ",".join(
            [
                dt
                for dt in ["current", "minutely", "hourly", "daily"]
                if dt != detailing_type
            ]
        )
        if exclude:
            url += f"&exclude={exclude}"

        response = requests.get(url)
        if response.status_code != 200:
            logger.error(f"Failed to fetch data from OpenWeatherMap: {response.text}")
            return None
        return response.json()
