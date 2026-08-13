import os
import requests

def get_weather(city=None, lat=None, lon=None):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENWEATHER_API_KEY is not configured")

    params = {"appid": api_key, "units": "metric"}
    if city:
        params["q"] = city
    else:
        params["lat"] = lat
        params["lon"] = lon

    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather",
        params=params,
        timeout=10
    )
    response.raise_for_status()
    data = response.json()

    return {
        "location": data.get("name"),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "pressure": data["main"]["pressure"],
        "wind_speed": data.get("wind", {}).get("speed", 0),
        "rainfall_mm": data.get("rain", {}).get("1h", 0),
        "description": data.get("weather", [{}])[0].get("description")
    }
