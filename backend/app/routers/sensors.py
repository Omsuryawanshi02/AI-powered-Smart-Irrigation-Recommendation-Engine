from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db

router = APIRouter(prefix="/api/fields/{field_id}/sensors", tags=["sensors"])


def _get_field_or_404(field_id: int, db: Session) -> models.Field:
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    return field


@router.post("", response_model=schemas.SensorReadingOut, status_code=201)
def add_sensor_reading(field_id: int, payload: schemas.SensorReadingCreate, db: Session = Depends(get_db)):
    _get_field_or_404(field_id, db)
    reading = models.SensorReading(field_id=field_id, **payload.model_dump())
    db.add(reading)
    db.commit()
    db.refresh(reading)
    return reading


@router.get("", response_model=List[schemas.SensorReadingOut])
def list_sensor_readings(field_id: int, limit: int = 50, db: Session = Depends(get_db)):
    _get_field_or_404(field_id, db)
    return (
        db.query(models.SensorReading)
        .filter(models.SensorReading.field_id == field_id)
        .order_by(models.SensorReading.recorded_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/latest", response_model=schemas.SensorReadingOut)
def latest_sensor_reading(field_id: int, db: Session = Depends(get_db)):
    _get_field_or_404(field_id, db)
    reading = (
        db.query(models.SensorReading)
        .filter(models.SensorReading.field_id == field_id)
        .order_by(models.SensorReading.recorded_at.desc())
        .first()
    )
    if not reading:
        raise HTTPException(404, "No sensor readings recorded for this field yet")
    return reading
