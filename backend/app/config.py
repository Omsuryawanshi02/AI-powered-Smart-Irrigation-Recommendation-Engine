import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Database
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'irrigation.db'}")

# ML model package (contains the trained sklearn/xgboost Pipeline + label mapping)
MODEL_PATH = os.getenv("MODEL_PATH", str(BASE_DIR / "models" / "irrigation_model_package.pkl"))

# Weather (Open-Meteo, free, no API key required)
WEATHER_API_URL = os.getenv("WEATHER_API_URL", "https://api.open-meteo.com/v1/forecast")
WEATHER_REQUEST_TIMEOUT = float(os.getenv("WEATHER_REQUEST_TIMEOUT", "6"))

# CORS - comma separated list of allowed origins, "*" for all
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# Baseline (traditional fixed-schedule) irrigation depth used for water-savings analytics, in mm
BASELINE_IRRIGATION_MM = float(os.getenv("BASELINE_IRRIGATION_MM", "25"))
BASELINE_INTERVAL_DAYS = int(os.getenv("BASELINE_INTERVAL_DAYS", "3"))
