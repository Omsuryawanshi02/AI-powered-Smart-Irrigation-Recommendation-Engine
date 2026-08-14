from datetime import datetime, date, timedelta
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, weather_service
from ..database import get_db
from ..ml.model_loader import predict_irrigation_need
from ..recommendation import generate_recommendation

router = APIRouter(prefix="/api/fields/{field_id}", tags=["recommendations"])


def _get_field_or_404(field_id: int, db: Session) -> models.Field:
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    return field


def _latest_reading(field_id: int, db: Session) -> Optional[models.SensorReading]:
    return (
        db.query(models.SensorReading)
        .filter(models.SensorReading.field_id == field_id)
        .order_by(models.SensorReading.recorded_at.desc())
        .first()
    )


def _estimate_water_mm(priority: str, soil_moisture: float) -> float:
    """Rough irrigation depth estimate (mm) — kept simple/transparent for a
    prototype; swap in a crop-water-balance model for production use."""
    if priority == "High":
        deficit = max(0.0, 50 - soil_moisture)
        return round(15 + deficit * 0.4, 1)
    if priority == "Medium":
        deficit = max(0.0, 40 - soil_moisture)
        return round(8 + deficit * 0.3, 1)
    return 0.0


def _build_feature_row(field: models.Field, reading: Optional[models.SensorReading],
                        overrides: schemas.RecommendationRequest, weather: dict) -> dict:
    def pick(*values, default=None):
        for v in values:
            if v is not None:
                return v
        return default

    return {
        "soil_ph": pick(overrides.soil_ph, reading.soil_ph if reading else None, default=6.5),
        "soil_moisture": pick(overrides.soil_moisture, reading.soil_moisture if reading else None, default=35.0),
        "organic_carbon": pick(overrides.organic_carbon, reading.organic_carbon if reading else None, default=0.8),
        "electrical_conductivity": pick(
            overrides.electrical_conductivity, reading.electrical_conductivity if reading else None, default=1.0
        ),
        "temperature_c": pick(
            overrides.temperature_c, reading.temperature_c if reading else None, weather.get("temperature_c"),
            default=28.0,
        ),
        "humidity": pick(
            overrides.humidity, reading.humidity if reading else None, weather.get("humidity"), default=55.0
        ),
        "rainfall_mm": pick(
            overrides.rainfall_mm, reading.rainfall_mm if reading else None, weather.get("rainfall_mm"), default=0.0
        ),
        "sunlight_hours": pick(
            overrides.sunlight_hours, reading.sunlight_hours if reading else None, weather.get("sunlight_hours"),
            default=8.0,
        ),
        "wind_speed_kmh": pick(
            overrides.wind_speed_kmh, reading.wind_speed_kmh if reading else None, weather.get("wind_speed_kmh"),
            default=8.0,
        ),
        "field_area_hectare": field.field_area_hectare,
        "previous_irrigation_mm": pick(
            overrides.previous_irrigation_mm, reading.previous_irrigation_mm if reading else None, default=0.0
        ),
        "soil_type": field.soil_type,
        "crop_type": field.crop_type,
        "crop_growth_stage": field.crop_growth_stage,
        "season": field.season,
        "mulching_used": "Yes" if field.mulching_used else "No",
        "region": field.region,
    }, pick(overrides.rain_forecast, weather.get("rain_forecast"), default=20.0)


@router.post("/recommendations/generate", response_model=schemas.RecommendationOut)
def generate_field_recommendation(
    field_id: int,
    payload: schemas.RecommendationRequest = schemas.RecommendationRequest(),
    db: Session = Depends(get_db),
):
    field = _get_field_or_404(field_id, db)
    reading = _latest_reading(field_id, db)
    weather = weather_service.get_weather(field.latitude, field.longitude)

    features, rain_forecast = _build_feature_row(field, reading, payload, weather)
    ml_result = predict_irrigation_need(features)

    rec_dict = generate_recommendation(
        irrigation_need=ml_result["irrigation_need"],
        soil_moisture=features["soil_moisture"],
        rain_forecast=rain_forecast,
        temperature=features["temperature_c"],
        humidity=features["humidity"],
        rainfall=features["rainfall_mm"],
    )

    water_mm = _estimate_water_mm(rec_dict["priority"], features["soil_moisture"])

    recommendation = models.Recommendation(
        field_id=field_id,
        sensor_reading_id=reading.id if reading else None,
        irrigation_need=rec_dict["irrigation_need"],
        status=rec_dict["status"],
        priority=rec_dict["priority"],
        action=rec_dict["action"],
        reason=rec_dict["reason"],
        recommended_water_mm=water_mm,
        soil_moisture=rec_dict["soil_moisture"],
        rain_forecast=rec_dict["rain_forecast"],
        temperature_c=features["temperature_c"],
        humidity=features["humidity"],
        model_confidence=ml_result.get("confidence"),
    )
    db.add(recommendation)
    db.commit()
    db.refresh(recommendation)

    # Auto-generate a mobile alert for anything actionable
    if recommendation.priority in ("High", "Medium"):
        severity = "critical" if recommendation.priority == "High" else "warning"
        alert = models.Alert(
            field_id=field_id,
            recommendation_id=recommendation.id,
            title=f"{recommendation.status} - {field.name}",
            message=f"{recommendation.action}. {recommendation.reason}",
            severity=severity,
        )
        db.add(alert)
        db.commit()

    return recommendation


@router.get("/recommendations", response_model=List[schemas.RecommendationOut])
def list_recommendations(field_id: int, limit: int = 20, db: Session = Depends(get_db)):
    _get_field_or_404(field_id, db)
    return (
        db.query(models.Recommendation)
        .filter(models.Recommendation.field_id == field_id)
        .order_by(models.Recommendation.created_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/recommendations/latest", response_model=schemas.RecommendationOut)
def latest_recommendation(field_id: int, db: Session = Depends(get_db)):
    _get_field_or_404(field_id, db)
    rec = (
        db.query(models.Recommendation)
        .filter(models.Recommendation.field_id == field_id)
        .order_by(models.Recommendation.created_at.desc())
        .first()
    )
    if not rec:
        raise HTTPException(404, "No recommendations generated for this field yet")
    return rec


@router.get("/schedule", response_model=schemas.ScheduleOut)
def irrigation_schedule(field_id: int, days: int = 5, db: Session = Depends(get_db)):
    """
    Forward-looking irrigation schedule for the next `days` days, built from
    the multi-day weather forecast plus the field's latest known soil
    moisture, decayed a little each day it isn't irrigated.
    """
    field = _get_field_or_404(field_id, db)
    reading = _latest_reading(field_id, db)
    forecast = weather_service.get_forecast(field.latitude, field.longitude, days)

    soil_moisture = reading.soil_moisture if reading else 35.0
    schedule_days = []

    for i, day_forecast in enumerate(forecast):
        rain_forecast = day_forecast.get("precipitation_probability_max") or 0
        temperature = day_forecast.get("temperature_2m_max")
        rainfall = day_forecast.get("precipitation_sum") or 0

        features = {
            "soil_moisture": soil_moisture,
            "temperature_c": temperature,
            "rainfall_mm": rainfall,
        }
        ml_result = predict_irrigation_need({
            **features,
            "soil_ph": reading.soil_ph if reading else 6.5,
            "organic_carbon": reading.organic_carbon if reading else 0.8,
            "electrical_conductivity": reading.electrical_conductivity if reading else 1.0,
            "humidity": None,
            "sunlight_hours": None,
            "wind_speed_kmh": None,
            "field_area_hectare": field.field_area_hectare,
            "previous_irrigation_mm": 0.0,
            "soil_type": field.soil_type,
            "crop_type": field.crop_type,
            "crop_growth_stage": field.crop_growth_stage,
            "season": field.season,
            "mulching_used": "Yes" if field.mulching_used else "No",
            "region": field.region,
        })

        rec = generate_recommendation(
            irrigation_need=ml_result["irrigation_need"],
            soil_moisture=soil_moisture,
            rain_forecast=rain_forecast,
            temperature=temperature,
        )
        water_mm = _estimate_water_mm(rec["priority"], soil_moisture)

        day_date = day_forecast.get("date")
        schedule_days.append(schemas.ScheduleDay(
            date=date.fromisoformat(day_date) if day_date else date.today() + timedelta(days=i),
            action=rec["action"],
            priority=rec["priority"],
            recommended_water_mm=water_mm,
            reason=rec["reason"],
        ))

        # Simulate next day's moisture: irrigation/rain replenish it, otherwise it decays.
        if water_mm > 0:
            soil_moisture = min(100, soil_moisture + water_mm * 0.8)
        else:
            soil_moisture = max(0, soil_moisture - 4 + min(rainfall, 10) * 0.5)

    return schemas.ScheduleOut(field_id=field_id, generated_at=datetime.utcnow(), days=schedule_days)
