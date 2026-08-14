from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from .. import weather_service

router = APIRouter(prefix="/api/weather", tags=["weather"])


@router.get("/current", response_model=schemas.WeatherOut)
def current_weather(
    latitude: float = Query(...),
    longitude: float = Query(...),
):
    return weather_service.get_weather(latitude, longitude)


@router.get("/fields/{field_id}", response_model=schemas.WeatherOut)
def current_weather_for_field(field_id: int, db: Session = Depends(get_db)):
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    return weather_service.get_weather(field.latitude, field.longitude)


@router.get("/fields/{field_id}/forecast")
def forecast_for_field(field_id: int, days: int = 5, db: Session = Depends(get_db)):
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    return {"field_id": field_id, "forecast": weather_service.get_forecast(field.latitude, field.longitude, days)}
