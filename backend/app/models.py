from datetime import datetime, date

from sqlalchemy import (
    Column, Integer, String, Float, DateTime, Date, Boolean, Text, ForeignKey
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    fields = relationship("Field", back_populates="owner", cascade="all, delete-orphan")


class Field(Base):
    """A single farm field / plot belonging to a user."""
    __tablename__ = "fields"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)

    # Crop info
    crop_type = Column(String, nullable=False)          # Wheat, Rice, Maize, Cotton, Sugarcane, Potato
    crop_growth_stage = Column(String, default="Sowing")  # Sowing, Vegetative, Flowering, Harvest
    sowing_date = Column(Date, nullable=True)

    # Field / soil info
    field_area_hectare = Column(Float, nullable=False)
    soil_type = Column(String, default="Loamy")          # Clay, Loamy, Sandy, Silt
    region = Column(String, default="Central")           # North, South, East, West, Central
    season = Column(String, nullable=True)                # Kharif, Rabi, Zaid (auto-derived if blank)
    irrigation_type = Column(String, default="Drip")      # Canal, Drip, Rainfed, Sprinkler
    water_source = Column(String, default="Groundwater")  # Groundwater, Rainwater, Reservoir, River
    mulching_used = Column(Boolean, default=False)

    # Location, used to fetch live weather
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    owner = relationship("User", back_populates="fields")
    sensor_readings = relationship("SensorReading", back_populates="field", cascade="all, delete-orphan")
    recommendations = relationship("Recommendation", back_populates="field", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="field", cascade="all, delete-orphan")
    water_logs = relationship("WaterUsageLog", back_populates="field", cascade="all, delete-orphan")


class SensorReading(Base):
    """A soil-moisture / soil-sensor reading for a field (real IoT sensor or manual entry)."""
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)

    soil_moisture = Column(Float, nullable=False)          # %
    soil_ph = Column(Float, default=6.5)
    organic_carbon = Column(Float, default=0.8)
    electrical_conductivity = Column(Float, default=1.0)
    previous_irrigation_mm = Column(Float, default=0.0)

    # Optional local sensor readings (falls back to live weather if not supplied)
    temperature_c = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    wind_speed_kmh = Column(Float, nullable=True)
    sunlight_hours = Column(Float, nullable=True)
    rainfall_mm = Column(Float, nullable=True)

    recorded_at = Column(DateTime, default=datetime.utcnow)

    field = relationship("Field", back_populates="sensor_readings")


class Recommendation(Base):
    """Output of the AI irrigation recommendation engine for a field at a point in time."""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    sensor_reading_id = Column(Integer, ForeignKey("sensor_readings.id"), nullable=True)

    irrigation_need = Column(String, nullable=False)   # Low / Medium / High (raw ML output)
    status = Column(String, nullable=False)            # e.g. "Irrigation Required"
    priority = Column(String, nullable=False)           # Low / Medium / High
    action = Column(String, nullable=False)             # e.g. "Irrigate now"
    reason = Column(Text, nullable=False)
    recommended_water_mm = Column(Float, nullable=True)

    soil_moisture = Column(Float, nullable=False)
    rain_forecast = Column(Float, nullable=False)
    temperature_c = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)

    model_confidence = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    field = relationship("Field", back_populates="recommendations")


class Alert(Base):
    """Mobile-style alert/notification generated for a field."""
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=True)

    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    severity = Column(String, default="info")  # info / warning / critical
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    field = relationship("Field", back_populates="alerts")


class WaterUsageLog(Base):
    """A record of water actually applied to a field (for analytics / savings tracking)."""
    __tablename__ = "water_usage_logs"

    id = Column(Integer, primary_key=True, index=True)
    field_id = Column(Integer, ForeignKey("fields.id"), nullable=False)
    recommendation_id = Column(Integer, ForeignKey("recommendations.id"), nullable=True)

    water_applied_mm = Column(Float, nullable=False)
    water_applied_liters = Column(Float, nullable=True)
    source = Column(String, default="manual")  # manual / recommended / sensor
    logged_at = Column(DateTime, default=datetime.utcnow)

    field = relationship("Field", back_populates="water_logs")
