"""
Live weather integration for the irrigation engine.

Uses Open-Meteo (https://open-meteo.com) — a free weather API that requires
no API key — for current conditions and short-term rain forecast. If the
request fails (no network, field has no coordinates, etc.) a neutral mock
reading is returned so the rest of the pipeline keeps working end-to-end.
"""
import logging
from datetime import datetime
from typing import Optional

import requests

from .config import WEATHER_API_URL, WEATHER_REQUEST_TIMEOUT

logger = logging.getLogger("irrigation.weather")


def _mock_weather(lat: float, lon: float) -> dict:
    return {
        "latitude": lat,
        "longitude": lon,
        "temperature_c": 28.0,
        "humidity": 55.0,
        "wind_speed_kmh": 8.0,
        "rainfall_mm": 0.0,
        "rain_forecast": 20.0,
        "sunlight_hours": 8.0,
        "source": "mock (weather API unavailable)",
        "fetched_at": datetime.utcnow(),
    }


def get_weather(latitude: Optional[float], longitude: Optional[float]) -> dict:
    if latitude is None or longitude is None:
        return _mock_weather(latitude or 0.0, longitude or 0.0)

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m",
        "daily": "precipitation_probability_max,precipitation_sum,sunshine_duration",
        "forecast_days": 1,
        "timezone": "auto",
    }

    try:
        resp = requests.get(WEATHER_API_URL, params=params, timeout=WEATHER_REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        current = data.get("current", {})
        daily = data.get("daily", {})

        sunshine_seconds = (daily.get("sunshine_duration") or [None])[0]
        sunlight_hours = round(sunshine_seconds / 3600, 2) if sunshine_seconds else None

        return {
            "latitude": latitude,
            "longitude": longitude,
            "temperature_c": current.get("temperature_2m"),
            "humidity": current.get("relative_humidity_2m"),
            "wind_speed_kmh": current.get("wind_speed_10m"),
            "rainfall_mm": current.get("precipitation", 0.0),
            "rain_forecast": (daily.get("precipitation_probability_max") or [0])[0],
            "sunlight_hours": sunlight_hours,
            "source": "open-meteo",
            "fetched_at": datetime.utcnow(),
        }
    except Exception as exc:  # noqa: BLE001
        logger.warning("Weather API call failed (%s); using mock data.", exc)
        return _mock_weather(latitude, longitude)


def get_forecast(latitude: Optional[float], longitude: Optional[float], days: int = 5) -> list[dict]:
    """Multi-day forecast used to build the irrigation schedule."""
    if latitude is None or longitude is None:
        return [
            {"date": None, "precipitation_probability_max": 20, "precipitation_sum": 0,
             "temperature_2m_max": 30, "temperature_2m_min": 20}
            for _ in range(days)
        ]

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "precipitation_probability_max,precipitation_sum,temperature_2m_max,temperature_2m_min",
        "forecast_days": days,
        "timezone": "auto",
    }

    try:
        resp = requests.get(WEATHER_API_URL, params=params, timeout=WEATHER_REQUEST_TIMEOUT)
        resp.raise_for_status()
        daily = resp.json().get("daily", {})
        dates = daily.get("time", [])
        out = []
        for i, d in enumerate(dates):
            out.append({
                "date": d,
                "precipitation_probability_max": (daily.get("precipitation_probability_max") or [0] * len(dates))[i],
                "precipitation_sum": (daily.get("precipitation_sum") or [0] * len(dates))[i],
                "temperature_2m_max": (daily.get("temperature_2m_max") or [None] * len(dates))[i],
                "temperature_2m_min": (daily.get("temperature_2m_min") or [None] * len(dates))[i],
            })
        return out
    except Exception as exc:  # noqa: BLE001
        logger.warning("Weather forecast call failed (%s); using mock data.", exc)
        return [
            {"date": None, "precipitation_probability_max": 20, "precipitation_sum": 0,
             "temperature_2m_max": 30, "temperature_2m_min": 20}
            for _ in range(days)
        ]
