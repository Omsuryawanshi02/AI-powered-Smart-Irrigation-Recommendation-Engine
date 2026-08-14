from collections import defaultdict
from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..config import BASELINE_IRRIGATION_MM, BASELINE_INTERVAL_DAYS

router = APIRouter(prefix="/api/fields/{field_id}", tags=["analytics"])


def _get_field_or_404(field_id: int, db: Session) -> models.Field:
    field = db.query(models.Field).get(field_id)
    if not field:
        raise HTTPException(404, "Field not found")
    return field


@router.post("/water-usage", response_model=schemas.WaterUsageOut, status_code=201)
def log_water_usage(field_id: int, payload: schemas.WaterUsageCreate, db: Session = Depends(get_db)):
    _get_field_or_404(field_id, db)
    log = models.WaterUsageLog(field_id=field_id, **payload.model_dump())
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


@router.get("/water-usage", response_model=List[schemas.WaterUsageOut])
def list_water_usage(field_id: int, limit: int = 100, db: Session = Depends(get_db)):
    _get_field_or_404(field_id, db)
    return (
        db.query(models.WaterUsageLog)
        .filter(models.WaterUsageLog.field_id == field_id)
        .order_by(models.WaterUsageLog.logged_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/analytics/timeseries", response_model=schemas.AnalyticsTimeseries)
def water_usage_timeseries(field_id: int, days: int = 30, db: Session = Depends(get_db)):
    _get_field_or_404(field_id, db)
    since = datetime.utcnow() - timedelta(days=days)
    logs = (
        db.query(models.WaterUsageLog)
        .filter(models.WaterUsageLog.field_id == field_id, models.WaterUsageLog.logged_at >= since)
        .all()
    )

    daily_totals = defaultdict(float)
    for log in logs:
        daily_totals[log.logged_at.date()] += log.water_applied_mm

    points = [
        schemas.DailyUsagePoint(date=d, water_applied_mm=round(total, 2))
        for d, total in sorted(daily_totals.items())
    ]
    return schemas.AnalyticsTimeseries(field_id=field_id, points=points)


@router.get("/analytics/summary", response_model=schemas.AnalyticsSummary)
def analytics_summary(field_id: int, days: int = 30, db: Session = Depends(get_db)):
    field = _get_field_or_404(field_id, db)
    since = datetime.utcnow() - timedelta(days=days)

    logs = (
        db.query(models.WaterUsageLog)
        .filter(models.WaterUsageLog.field_id == field_id, models.WaterUsageLog.logged_at >= since)
        .all()
    )
    total_mm = sum(l.water_applied_mm for l in logs)
    total_liters = sum(l.water_applied_liters or (l.water_applied_mm * field.field_area_hectare * 10000) for l in logs)
    irrigation_events = len(logs)

    # Baseline = what a traditional fixed-interval schedule would have used over the same period
    baseline_events = max(1, days // BASELINE_INTERVAL_DAYS)
    baseline_mm = baseline_events * BASELINE_IRRIGATION_MM

    water_saved_mm = max(0.0, baseline_mm - total_mm)
    water_saved_percent = round((water_saved_mm / baseline_mm) * 100, 1) if baseline_mm else 0.0

    readings = (
        db.query(models.SensorReading)
        .filter(models.SensorReading.field_id == field_id, models.SensorReading.recorded_at >= since)
        .all()
    )
    avg_moisture = round(sum(r.soil_moisture for r in readings) / len(readings), 2) if readings else None

    high_alerts = (
        db.query(models.Alert)
        .filter(
            models.Alert.field_id == field_id,
            models.Alert.severity == "critical",
            models.Alert.created_at >= since,
        )
        .count()
    )

    return schemas.AnalyticsSummary(
        field_id=field_id,
        period_days=days,
        total_water_applied_mm=round(total_mm, 2),
        total_water_applied_liters=round(total_liters, 1),
        baseline_water_mm=round(baseline_mm, 2),
        water_saved_mm=round(water_saved_mm, 2),
        water_saved_percent=water_saved_percent,
        irrigation_events=irrigation_events,
        avg_soil_moisture=avg_moisture,
        high_priority_alerts=high_alerts,
    )
