# Weather Forecast App

## Overview

The Weather Forecast App is a Django application that fetches weather data from the OpenWeatherMap API and serves it through a custom API endpoint. The app stores recent weather data in a PostgreSQL database to minimize the number of requests made to the external API.

## Features

- Fetch weather data based on latitude and longitude coordinates.
- Support for different detailing types: current weather, minutely forecast, hourly forecast, and daily forecast.
- Caching mechanism to store recent weather data and reduce external API calls.
- Dockerized setup for easy deployment.
- Environment variables for configuration.

## Tech Stack
- Pyhton
- Django
- PostgreSQL
- Docker

## Setup

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Environment Variables

Create a `.env` file in the root directory of the project and add the following variables:

# Django settings
SECRET_KEY=6ba2a0b4351b142ewdckj23bsdhsdcjhwdcwdjchwjj
DEBUG=True
ALLOWED_HOSTS=127.0.0.1

# Database configuration
POSTGRES_DB=weatherdb
POSTGRES_USER=weatheruser
POSTGRES_PASSWORD=password


OPENWEATHERMAP_API_KEY=32a8a7abd422841f6ba2a0b4351b142e
CACHE_DURATION=10



### Docker Setup

1. Build and run the Docker containers:

```bash
docker-compose up --build

GET WEATHER DATA by below URL
GET api/weather/?lat=33.441792&lon=-94.037689&detailing_type=current


