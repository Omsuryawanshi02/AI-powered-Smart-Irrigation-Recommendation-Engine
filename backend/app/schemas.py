from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field as PydField, ConfigDict


# ---------------------------------------------------------------------------
# Users
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    name: str
    phone: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    phone: str
    created_at: datetime


# ---------------------------------------------------------------------------
# Fields
# ---------------------------------------------------------------------------

class FieldCreate(BaseModel):
    user_id: int
    name: str
    crop_type: str
    crop_growth_stage: Optional[str] = "Sowing"
    sowing_date: Optional[date] = None

    # size can be given in acre or hectare; converted & stored as hectares
    field_size: float
    size_unit: str = "hectare"  # "hectare" | "acre"

    soil_type: Optional[str] = "Loamy"
    region: Optional[str] = "Central"
    season: Optional[str] = None
    irrigation_type: Optional[str] = "Drip"
    water_source: Optional[str] = "Groundwater"
    mulching_used: Optional[bool] = False

    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FieldUpdate(BaseModel):
    name: Optional[str] = None
    crop_type: Optional[str] = None
    crop_growth_stage: Optional[str] = None
    sowing_date: Optional[date] = None
    field_area_hectare: Optional[float] = None
    soil_type: Optional[str] = None
    region: Optional[str] = None
    season: Optional[str] = None
    irrigation_type: Optional[str] = None
    water_source: Optional[str] = None
    mulching_used: Optional[bool] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FieldOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    user_id: int
    name: str
    crop_type: str
    crop_growth_stage: str
    sowing_date: Optional[date]
    field_area_hectare: float
    soil_type: str
    region: str
    season: Optional[str]
    irrigation_type: str
    water_source: str
    mulching_used: bool
    latitude: Optional[float]
    longitude: Optional[float]
    created_at: datetime


# ---------------------------------------------------------------------------
# Sensor readings
# ---------------------------------------------------------------------------

class SensorReadingCreate(BaseModel):
    soil_moisture: float = PydField(..., ge=0, le=100)
    soil_ph: Optional[float] = 6.5
    organic_carbon: Optional[float] = 0.8
    electrical_conductivity: Optional[float] = 1.0
    previous_irrigation_mm: Optional[float] = 0.0

    # Optional on-field sensor values; if omitted, live weather API fills these in
    temperature_c: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    sunlight_hours: Optional[float] = None
    rainfall_mm: Optional[float] = None


class SensorReadingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    field_id: int
    soil_moisture: float
    soil_ph: float
    organic_carbon: float
    electrical_conductivity: float
    previous_irrigation_mm: float
    temperature_c: Optional[float]
    humidity: Optional[float]
    wind_speed_kmh: Optional[float]
    sunlight_hours: Optional[float]
    rainfall_mm: Optional[float]
    recorded_at: datetime


# ---------------------------------------------------------------------------
# Recommendations
# ---------------------------------------------------------------------------

class RecommendationRequest(BaseModel):
    """Optional manual overrides. Any field left blank is filled in from the
    field's latest sensor reading and/or live weather data."""
    soil_moisture: Optional[float] = None
    soil_ph: Optional[float] = None
    organic_carbon: Optional[float] = None
    electrical_conductivity: Optional[float] = None
    previous_irrigation_mm: Optional[float] = None
    temperature_c: Optional[float] = None
    humidity: Optional[float] = None
    wind_speed_kmh: Optional[float] = None
    sunlight_hours: Optional[float] = None
    rainfall_mm: Optional[float] = None
    rain_forecast: Optional[float] = None  # 0-100, probability/intensity of near-term rain


class RecommendationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    field_id: int
    irrigation_need: str
    status: str
    priority: str
    action: str
    reason: str
    recommended_water_mm: Optional[float]
    soil_moisture: float
    rain_forecast: float
    temperature_c: Optional[float]
    humidity: Optional[float]
    model_confidence: Optional[float]
    created_at: datetime


class ScheduleDay(BaseModel):
    date: date
    action: str
    priority: str
    recommended_water_mm: Optional[float]
    reason: str


class ScheduleOut(BaseModel):
    field_id: int
    generated_at: datetime
    days: List[ScheduleDay]


# ---------------------------------------------------------------------------
# Alerts
# ---------------------------------------------------------------------------

class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    field_id: int
    recommendation_id: Optional[int]
    title: str
    message: str
    severity: str
    is_read: bool
    created_at: datetime


# ---------------------------------------------------------------------------
# Water usage / analytics
# ---------------------------------------------------------------------------

class WaterUsageCreate(BaseModel):
    water_applied_mm: float
    water_applied_liters: Optional[float] = None
    source: Optional[str] = "manual"
    recommendation_id: Optional[int] = None


class WaterUsageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    field_id: int
    recommendation_id: Optional[int]
    water_applied_mm: float
    water_applied_liters: Optional[float]
    source: str
    logged_at: datetime


class AnalyticsSummary(BaseModel):
    field_id: int
    period_days: int
    total_water_applied_mm: float
    total_water_applied_liters: float
    baseline_water_mm: float
    water_saved_mm: float
    water_saved_percent: float
    irrigation_events: int
    avg_soil_moisture: Optional[float]
    high_priority_alerts: int


class DailyUsagePoint(BaseModel):
    date: date
    water_applied_mm: float


class AnalyticsTimeseries(BaseModel):
    field_id: int
    points: List[DailyUsagePoint]


# ---------------------------------------------------------------------------
# Weather
# ---------------------------------------------------------------------------

class WeatherOut(BaseModel):
    latitude: float
    longitude: float
    temperature_c: Optional[float]
    humidity: Optional[float]
    wind_speed_kmh: Optional[float]
    rainfall_mm: Optional[float]
    rain_forecast: Optional[float]
    sunlight_hours: Optional[float]
    source: str
    fetched_at: datetime
